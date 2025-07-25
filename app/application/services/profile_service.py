from typing import List, Optional
from domain.entities.profile import Profile
from domain.repositories.profile_repository import ProfileRepository
from domain.repositories.role_repository import RoleRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse

class ProfileService:
    def __init__(self, profile_repository: ProfileRepository, role_repository: RoleRepository):
        self.profile_repository = profile_repository
        self.role_repository = role_repository

    def create_profile(self, profile_data: ProfileCreate) -> ProfileResponse:
        """Criar um novo profile"""
        # Verificar se o role existe
        role = self.role_repository.get_by_id(profile_data.role_id)
        if not role:
            raise ValueError("Role não encontrado")

        # Criar entidade de domínio
        profile = Profile(
            user_id=profile_data.user_id,
            role_id=profile_data.role_id,
            full_name=profile_data.full_name,
            artistic_name=profile_data.artistic_name,
            bio=profile_data.bio,
            cep=profile_data.cep,
            logradouro=profile_data.logradouro,
            numero=profile_data.numero,
            cidade=profile_data.cidade,
            uf=profile_data.uf,
            telefone_movel=profile_data.telefone_movel,
            complemento=profile_data.complemento,
            telefone_fixo=profile_data.telefone_fixo,
            whatsapp=profile_data.whatsapp,
            latitude=profile_data.latitude,
            longitude=profile_data.longitude
        )

        # Salvar no repositório
        created_profile = self.profile_repository.create(profile)
        
        # Converter para schema de resposta
        return ProfileResponse(
            id=created_profile.id,
            user_id=created_profile.user_id,
            role_id=created_profile.role_id,
            full_name=created_profile.full_name,
            artistic_name=created_profile.artistic_name,
            bio=created_profile.bio,
            cep=created_profile.cep,
            logradouro=created_profile.logradouro,
            numero=created_profile.numero,
            complemento=created_profile.complemento,
            cidade=created_profile.cidade,
            uf=created_profile.uf,
            telefone_fixo=created_profile.telefone_fixo,
            telefone_movel=created_profile.telefone_movel,
            whatsapp=created_profile.whatsapp,
            latitude=created_profile.latitude,
            longitude=created_profile.longitude,
            created_at=created_profile.created_at,
            updated_at=created_profile.updated_at
        )

    def get_profiles(self, skip: int = 0, limit: int = 100) -> List[ProfileResponse]:
        """Listar profiles com paginação"""
        profiles = self.profile_repository.get_all(skip=skip, limit=limit)
        return [
            ProfileResponse(
                id=profile.id,
                user_id=profile.user_id,
                role_id=profile.role_id,
                full_name=profile.full_name,
                artistic_name=profile.artistic_name,
                bio=profile.bio,
                cep=profile.cep,
                logradouro=profile.logradouro,
                numero=profile.numero,
                complemento=profile.complemento,
                cidade=profile.cidade,
                uf=profile.uf,
                telefone_fixo=profile.telefone_fixo,
                telefone_movel=profile.telefone_movel,
                whatsapp=profile.whatsapp,
                latitude=profile.latitude,
                longitude=profile.longitude,
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
            for profile in profiles
        ]

    def get_profile_by_id(self, profile_id: int) -> Optional[ProfileResponse]:
        """Obter profile por ID"""
        profile = self.profile_repository.get_by_id(profile_id)
        if not profile:
            return None
        
        return ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            role_id=profile.role_id,
            full_name=profile.full_name,
            artistic_name=profile.artistic_name,
            bio=profile.bio,
            cep=profile.cep,
            logradouro=profile.logradouro,
            numero=profile.numero,
            complemento=profile.complemento,
            cidade=profile.cidade,
            uf=profile.uf,
            telefone_fixo=profile.telefone_fixo,
            telefone_movel=profile.telefone_movel,
            whatsapp=profile.whatsapp,
            latitude=profile.latitude,
            longitude=profile.longitude,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileResponse]:
        """Obter profile por user_id"""
        profile = self.profile_repository.get_by_user_id(user_id)
        if not profile:
            return None
        
        return ProfileResponse(
            id=profile.id,
            role_id=profile.role_id,
            full_name=profile.full_name,
            artistic_name=profile.artistic_name,
            bio=profile.bio,
            cep=profile.cep,
            logradouro=profile.logradouro,
            numero=profile.numero,
            complemento=profile.complemento,
            cidade=profile.cidade,
            uf=profile.uf,
            telefone_fixo=profile.telefone_fixo,
            telefone_movel=profile.telefone_movel,
            whatsapp=profile.whatsapp,
            latitude=profile.latitude,
            longitude=profile.longitude,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    def get_profiles_by_role_id(self, role_id: int) -> List[ProfileResponse]:
        """Obter profiles por role_id"""
        profiles = self.profile_repository.get_by_role_id(role_id)
        return [
            ProfileResponse(
                id=profile.id,
                role_id=profile.role_id,
                full_name=profile.full_name,
                artistic_name=profile.artistic_name,
                bio=profile.bio,
                cep=profile.cep,
                logradouro=profile.logradouro,
                numero=profile.numero,
                complemento=profile.complemento,
                cidade=profile.cidade,
                uf=profile.uf,
                telefone_fixo=profile.telefone_fixo,
                telefone_movel=profile.telefone_movel,
                whatsapp=profile.whatsapp,
                latitude=profile.latitude,
                longitude=profile.longitude,
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
            for profile in profiles
        ]

    def update_profile(self, profile_id: int, profile_data: ProfileUpdate) -> Optional[ProfileResponse]:
        """Atualizar profile"""
        profile = self.profile_repository.get_by_id(profile_id)
        if not profile:
            return None

        # Verificar se o novo role existe (se fornecido)
        if profile_data.role_id is not None:
            role = self.role_repository.get_by_id(profile_data.role_id)
            if not role:
                raise ValueError("Role não encontrado")
            profile.role_id = profile_data.role_id

        # Atualizar campos fornecidos
        if profile_data.full_name is not None:
            profile.full_name = profile_data.full_name
        if profile_data.artistic_name is not None:
            profile.artistic_name = profile_data.artistic_name
        if profile_data.bio is not None:
            profile.bio = profile_data.bio
        if profile_data.cep is not None:
            profile.cep = profile_data.cep
        if profile_data.logradouro is not None:
            profile.logradouro = profile_data.logradouro
        if profile_data.numero is not None:
            profile.numero = profile_data.numero
        if profile_data.complemento is not None:
            profile.complemento = profile_data.complemento
        if profile_data.cidade is not None:
            profile.cidade = profile_data.cidade
        if profile_data.uf is not None:
            profile.uf = profile_data.uf
        if profile_data.telefone_fixo is not None:
            profile.telefone_fixo = profile_data.telefone_fixo
        if profile_data.telefone_movel is not None:
            profile.telefone_movel = profile_data.telefone_movel
        if profile_data.whatsapp is not None:
            profile.whatsapp = profile_data.whatsapp
        if profile_data.latitude is not None:
            profile.latitude = profile_data.latitude
        if profile_data.longitude is not None:
            profile.longitude = profile_data.longitude

        # Salvar alterações
        updated_profile = self.profile_repository.update(profile)
        
        return ProfileResponse(
            id=updated_profile.id,
            role_id=updated_profile.role_id,
            full_name=updated_profile.full_name,
            artistic_name=updated_profile.artistic_name,
            bio=updated_profile.bio,
            cep=updated_profile.cep,
            logradouro=updated_profile.logradouro,
            numero=updated_profile.numero,
            complemento=updated_profile.complemento,
            cidade=updated_profile.cidade,
            uf=updated_profile.uf,
            telefone_fixo=updated_profile.telefone_fixo,
            telefone_movel=updated_profile.telefone_movel,
            whatsapp=updated_profile.whatsapp,
            latitude=updated_profile.latitude,
            longitude=updated_profile.longitude,
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at
        )

    def delete_profile(self, profile_id: int) -> bool:
        """Deletar profile"""
        return self.profile_repository.delete(profile_id) 