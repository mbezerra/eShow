from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories.artist_repository import ArtistRepository
from domain.repositories.space_repository import SpaceRepository
from domain.repositories.profile_repository import ProfileRepository
from domain.repositories.space_event_type_repository import SpaceEventTypeRepository
from domain.repositories.space_festival_type_repository import SpaceFestivalTypeRepository
from domain.repositories.booking_repository import BookingRepository
from domain.entities.space_event_type import StatusEventType
from domain.entities.space_festival_type import StatusFestivalType
from app.core.location_utils import LocationUtils
from app.schemas.location_search import (
    LocationSearchResponse,
    SpaceLocationResult,
    ArtistLocationResult,
    ProfileLocationResult
)

class LocationSearchService:
    """Serviço para busca por localização"""
    
    def __init__(
        self,
        artist_repository: ArtistRepository,
        space_repository: SpaceRepository,
        profile_repository: ProfileRepository,
        space_event_type_repository: SpaceEventTypeRepository,
        space_festival_type_repository: SpaceFestivalTypeRepository,
        booking_repository: BookingRepository
    ):
        self.artist_repository = artist_repository
        self.space_repository = space_repository
        self.profile_repository = profile_repository
        self.space_event_type_repository = space_event_type_repository
        self.space_festival_type_repository = space_festival_type_repository
        self.booking_repository = booking_repository
    
    def search_spaces_for_artist(
        self,
        db: Session,
        artist_profile_id: int,
        return_full_data: bool = True,
        max_results: Optional[int] = 100
    ) -> LocationSearchResponse:
        """
        Endpoint 1: Busca espaços para um artista baseado no raio de atuação do artista
        
        Args:
            db: Sessão do banco de dados
            artist_profile_id: ID do profile do artista logado
            return_full_data: Se deve retornar dados completos ou apenas IDs
            max_results: Limite máximo de resultados
            
        Returns:
            Lista de espaços disponíveis dentro do raio de atuação do artista
        """
        try:
            # 1. Obter dados do artista logado
            artist_profile = self.profile_repository.get_by_id(artist_profile_id)
            if not artist_profile:
                raise ValueError("Profile do artista não encontrado")
            
            artist = self.artist_repository.get_by_profile_id(artist_profile_id)
            if not artist:
                raise ValueError("Artista não encontrado")
            
            # 2. Obter coordenadas do artista (priorizando coordenadas do profile)
            artist_coords = LocationUtils.get_coordinates_from_profile(artist_profile)
            if not artist_coords:
                raise ValueError(f"Coordenadas não encontradas para o artista {artist_profile.id}")
            
            artist_lat, artist_lng = artist_coords
            
            # 3. Obter todos os profiles de espaços (role_id = 3)
            space_profiles = self.profile_repository.get_by_role_id(role_id=3)
            
            results = []
            total_count = 0
            
            for space_profile in space_profiles:
                # 4. Obter coordenadas do espaço (priorizando coordenadas do profile)
                space_coords = LocationUtils.get_coordinates_from_profile(space_profile)
                if not space_coords:
                    continue
                
                space_lat, space_lng = space_coords
                
                # 5. Calcular distância
                distance = LocationUtils.calculate_distance(
                    artist_lat, artist_lng, space_lat, space_lng
                )
                
                # 6. Verificar se está dentro do raio de atuação
                if distance <= artist.raio_atuacao:
                    # 7. Verificar se o espaço tem eventos/festivais com status CONTRATANDO
                    spaces = self.space_repository.get_by_profile_id(space_profile.id)
                    if spaces:
                        space = spaces[0]  # Pegar o primeiro espaço do profile
                        has_contracting_events = self._check_contracting_events(db, space.id)
                        
                        if has_contracting_events:
                            if return_full_data:
                                result = SpaceLocationResult(
                                    id=space.id,
                                    profile_id=space.profile_id,
                                    space_type_id=space.space_type_id,
                                    acesso=space.acesso,
                                    valor_hora=space.valor_hora,
                                    valor_couvert=space.valor_couvert,
                                    publico_estimado=space.publico_estimado,
                                    distance_km=distance,
                                    profile=ProfileLocationResult(
                                        id=space_profile.id,
                                        full_name=space_profile.full_name,
                                        artistic_name=space_profile.artistic_name,
                                        cep=space_profile.cep,
                                        cidade=space_profile.cidade,
                                        uf=space_profile.uf
                                    )
                                )
                            else:
                                result = SpaceLocationResult(
                                    id=space.id,
                                    distance_km=distance
                                )
                            
                            results.append(result)
                            total_count += 1
                            
                            if max_results and total_count >= max_results:
                                break
            
            return LocationSearchResponse(
                results=results,
                total_count=total_count,
                search_radius_km=artist.raio_atuacao,
                origin_cep=artist_profile.cep
            )
            
        except Exception as e:
            raise Exception(f"Erro na busca de espaços para artista: {str(e)}")
    
    def search_artists_for_space(
        self,
        db: Session,
        space_profile_id: int,
        return_full_data: bool = True,
        max_results: Optional[int] = 100
    ) -> LocationSearchResponse:
        """
        Endpoint 2: Busca artistas para um espaço baseado no raio de atuação dos artistas
        
        Args:
            db: Sessão do banco de dados
            space_profile_id: ID do profile do espaço logado
            return_full_data: Se deve retornar dados completos ou apenas IDs
            max_results: Limite máximo de resultados
            
        Returns:
            Lista de artistas disponíveis dentro do raio de atuação
        """
        try:
            # 1. Obter dados do espaço logado
            space_profile = self.profile_repository.get_by_id(space_profile_id)
            if not space_profile:
                raise ValueError("Profile do espaço não encontrado")
            
            spaces = self.space_repository.get_by_profile_id(space_profile_id)
            if not spaces:
                raise ValueError("Espaço não encontrado")
            space = spaces[0]  # Pegar o primeiro espaço do profile
            
            # 2. Obter coordenadas do espaço (priorizando coordenadas do profile)
            space_coords = LocationUtils.get_coordinates_from_profile(space_profile)
            if not space_coords:
                raise ValueError(f"Coordenadas não encontradas para o espaço {space_profile.id}")
            
            space_lat, space_lng = space_coords
            
            # 3. Obter todos os profiles de artistas (role_id = 2)
            artist_profiles = self.profile_repository.get_by_role_id(role_id=2)
            
            results = []
            total_count = 0
            
            for artist_profile in artist_profiles:
                # 4. Obter dados do artista
                artist = self.artist_repository.get_by_profile_id(artist_profile.id)
                if not artist:
                    continue
                
                # 5. Obter coordenadas do artista (priorizando coordenadas do profile)
                artist_coords = LocationUtils.get_coordinates_from_profile(artist_profile)
                if not artist_coords:
                    continue
                
                artist_lat, artist_lng = artist_coords
                
                # 6. Calcular distância
                distance = LocationUtils.calculate_distance(
                    space_lat, space_lng, artist_lat, artist_lng
                )
                
                # 7. Verificar se está dentro do raio de atuação do artista
                if distance <= artist.raio_atuacao:
                    # 8. Verificar se o artista não tem agendamentos conflitantes
                    is_available = self._check_artist_availability(
                        db, artist.id, space.id
                    )
                    
                    if is_available:
                        if return_full_data:
                            result = ArtistLocationResult(
                                id=artist.id,
                                profile_id=artist.profile_id,
                                artist_type_id=artist.artist_type_id,
                                raio_atuacao=artist.raio_atuacao,
                                valor_hora=artist.valor_hora,
                                valor_couvert=artist.valor_couvert,
                                distance_km=distance,
                                profile=ProfileLocationResult(
                                    id=artist_profile.id,
                                    full_name=artist_profile.full_name,
                                    artistic_name=artist_profile.artistic_name,
                                    cep=artist_profile.cep,
                                    cidade=artist_profile.cidade,
                                    uf=artist_profile.uf
                                )
                            )
                        else:
                            result = ArtistLocationResult(
                                id=artist.id,
                                distance_km=distance
                            )
                        
                        results.append(result)
                        total_count += 1
                        
                        if max_results and total_count >= max_results:
                            break
            
            return LocationSearchResponse(
                results=results,
                total_count=total_count,
                search_radius_km=0,  # Varia conforme o raio de cada artista
                origin_cep=space_profile.cep
            )
            
        except Exception as e:
            raise Exception(f"Erro na busca de artistas para espaço: {str(e)}")
    
    def _check_contracting_events(self, db: Session, space_id: int) -> bool:
        """
        Verifica se um espaço tem eventos ou festivais com status CONTRATANDO
        """
        # Verificar space_event_types
        event_types = self.space_event_type_repository.get_by_space_id_and_status(
            space_id, StatusEventType.CONTRATANDO
        )
        
        if event_types:
            return True
        
        # Verificar space_festival_types
        festival_types = self.space_festival_type_repository.get_by_space_id_and_status(
            space_id, StatusFestivalType.CONTRATANDO
        )
        
        return len(festival_types) > 0
    
    def _check_artist_availability(
        self,
        db: Session,
        artist_id: int,
        space_id: int
    ) -> bool:
        """
        Verifica se um artista está disponível para um espaço específico
        (não tem agendamentos conflitantes)
        """
        # Obter eventos e festivais do espaço com status CONTRATANDO
        contracting_events = self.space_event_type_repository.get_by_space_id_and_status(
            space_id, StatusEventType.CONTRATANDO
        )
        
        contracting_festivals = self.space_festival_type_repository.get_by_space_id_and_status(
            space_id, StatusFestivalType.CONTRATANDO
        )
        
        # Verificar conflitos para cada evento/festival
        for event in contracting_events:
            conflicting_bookings = self.booking_repository.get_conflicting_bookings(
                artist_id=artist_id,
                data=event.data,
                horario=event.horario
            )
            if conflicting_bookings:
                return False
        
        for festival in contracting_festivals:
            conflicting_bookings = self.booking_repository.get_conflicting_bookings(
                artist_id=artist_id,
                data=festival.data,
                horario=festival.horario
            )
            if conflicting_bookings:
                return False
        
        return True 