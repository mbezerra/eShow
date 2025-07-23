from typing import List, Optional, Union, TYPE_CHECKING
from domain.entities.space import Space
from domain.repositories.space_repository import SpaceRepository

if TYPE_CHECKING:
    from infrastructure.database.models.space_model import SpaceModel

class SpaceService:
    def __init__(self, space_repository: SpaceRepository):
        self.space_repository = space_repository

    def create_space(self, space_data: dict) -> Space:
        """Criar um novo espaço"""
        space = Space(
            profile_id=space_data["profile_id"],
            space_type_id=space_data["space_type_id"],
            event_type_id=space_data.get("event_type_id"),
            festival_type_id=space_data.get("festival_type_id"),
            acesso=space_data["acesso"],
            dias_apresentacao=space_data["dias_apresentacao"],
            duracao_apresentacao=space_data["duracao_apresentacao"],
            valor_hora=space_data["valor_hora"],
            valor_couvert=space_data["valor_couvert"],
            requisitos_minimos=space_data["requisitos_minimos"],
            oferecimentos=space_data["oferecimentos"],
            estrutura_apresentacao=space_data["estrutura_apresentacao"],
            publico_estimado=space_data["publico_estimado"],
            fotos_ambiente=space_data["fotos_ambiente"],
            instagram=space_data.get("instagram"),
            tiktok=space_data.get("tiktok"),
            youtube=space_data.get("youtube"),
            facebook=space_data.get("facebook")
        )
        return self.space_repository.create(space)

    def get_space_by_id(self, space_id: int, include_relations: bool = False) -> Optional[Union[Space, "SpaceModel"]]:
        """Buscar espaço por ID"""
        return self.space_repository.get_by_id(space_id, include_relations=include_relations)

    def get_spaces_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        """Buscar espaços por profile ID"""
        return self.space_repository.get_by_profile_id(profile_id, include_relations=include_relations)

    def get_spaces_by_space_type_id(self, space_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        """Buscar espaços por tipo de espaço"""
        return self.space_repository.get_by_space_type_id(space_type_id, include_relations=include_relations)

    def get_spaces_by_event_type_id(self, event_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        """Buscar espaços por tipo de evento"""
        return self.space_repository.get_by_event_type_id(event_type_id, include_relations=include_relations)

    def get_spaces_by_festival_type_id(self, festival_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        """Buscar espaços por tipo de festival"""
        return self.space_repository.get_by_festival_type_id(festival_type_id, include_relations=include_relations)

    def get_all_spaces(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        """Listar todos os espaços"""
        return self.space_repository.get_all(skip=skip, limit=limit, include_relations=include_relations)

    def update_space(self, space_id: int, space_data: dict) -> Space:
        """Atualizar um espaço"""
        space = self.space_repository.get_by_id(space_id)
        if not space:
            raise ValueError(f"Space with id {space_id} not found")

        # Atualizar campos
        space.profile_id = space_data["profile_id"]
        space.space_type_id = space_data["space_type_id"]
        space.event_type_id = space_data.get("event_type_id")
        space.festival_type_id = space_data.get("festival_type_id")
        space.acesso = space_data["acesso"]
        space.dias_apresentacao = space_data["dias_apresentacao"]
        space.duracao_apresentacao = space_data["duracao_apresentacao"]
        space.valor_hora = space_data["valor_hora"]
        space.valor_couvert = space_data["valor_couvert"]
        space.requisitos_minimos = space_data["requisitos_minimos"]
        space.oferecimentos = space_data["oferecimentos"]
        space.estrutura_apresentacao = space_data["estrutura_apresentacao"]
        space.publico_estimado = space_data["publico_estimado"]
        space.fotos_ambiente = space_data["fotos_ambiente"]
        space.instagram = space_data.get("instagram")
        space.tiktok = space_data.get("tiktok")
        space.youtube = space_data.get("youtube")
        space.facebook = space_data.get("facebook")

        return self.space_repository.update(space)

    def delete_space(self, space_id: int) -> bool:
        """Deletar um espaço"""
        return self.space_repository.delete(space_id) 