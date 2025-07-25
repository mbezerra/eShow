from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.profile import Profile
from domain.repositories.profile_repository import ProfileRepository
from infrastructure.database.models.profile_model import ProfileModel

class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, profile: Profile) -> Profile:
        """Criar um novo profile"""
        db_profile = ProfileModel(
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
            whatsapp=profile.whatsapp
        )
        self.session.add(db_profile)
        self.session.commit()
        self.session.refresh(db_profile)
        
        return Profile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            role_id=db_profile.role_id,
            full_name=db_profile.full_name,
            artistic_name=db_profile.artistic_name,
            bio=db_profile.bio,
            cep=db_profile.cep,
            logradouro=db_profile.logradouro,
            numero=db_profile.numero,
            complemento=db_profile.complemento,
            cidade=db_profile.cidade,
            uf=db_profile.uf,
            telefone_fixo=db_profile.telefone_fixo,
            telefone_movel=db_profile.telefone_movel,
            whatsapp=db_profile.whatsapp,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )

    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Obter profile por ID"""
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not db_profile:
            return None
        
        return Profile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            role_id=db_profile.role_id,
            full_name=db_profile.full_name,
            artistic_name=db_profile.artistic_name,
            bio=db_profile.bio,
            cep=db_profile.cep,
            logradouro=db_profile.logradouro,
            numero=db_profile.numero,
            complemento=db_profile.complemento,
            cidade=db_profile.cidade,
            uf=db_profile.uf,
            telefone_fixo=db_profile.telefone_fixo,
            telefone_movel=db_profile.telefone_movel,
            whatsapp=db_profile.whatsapp,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )

    def get_by_role_id(self, role_id: int) -> List[Profile]:
        """Obter profiles por role_id"""
        db_profiles = self.session.query(ProfileModel).filter(ProfileModel.role_id == role_id).all()
        return [
            Profile(
                id=db_profile.id,
                user_id=db_profile.user_id,
                role_id=db_profile.role_id,
                full_name=db_profile.full_name,
                artistic_name=db_profile.artistic_name,
                bio=db_profile.bio,
                cep=db_profile.cep,
                logradouro=db_profile.logradouro,
                numero=db_profile.numero,
                complemento=db_profile.complemento,
                cidade=db_profile.cidade,
                uf=db_profile.uf,
                telefone_fixo=db_profile.telefone_fixo,
                telefone_movel=db_profile.telefone_movel,
                whatsapp=db_profile.whatsapp,
                created_at=db_profile.created_at,
                updated_at=db_profile.updated_at
            )
            for db_profile in db_profiles
        ]

    def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """Obter profile por user_id"""
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.user_id == user_id).first()
        if not db_profile:
            return None
        
        return Profile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            role_id=db_profile.role_id,
            full_name=db_profile.full_name,
            artistic_name=db_profile.artistic_name,
            bio=db_profile.bio,
            cep=db_profile.cep,
            logradouro=db_profile.logradouro,
            numero=db_profile.numero,
            complemento=db_profile.complemento,
            cidade=db_profile.cidade,
            uf=db_profile.uf,
            telefone_fixo=db_profile.telefone_fixo,
            telefone_movel=db_profile.telefone_movel,
            whatsapp=db_profile.whatsapp,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Listar todos os profiles com paginação"""
        db_profiles = self.session.query(ProfileModel).offset(skip).limit(limit).all()
        return [
            Profile(
                id=db_profile.id,
                user_id=db_profile.user_id,
                role_id=db_profile.role_id,
                full_name=db_profile.full_name,
                artistic_name=db_profile.artistic_name,
                bio=db_profile.bio,
                cep=db_profile.cep,
                logradouro=db_profile.logradouro,
                numero=db_profile.numero,
                complemento=db_profile.complemento,
                cidade=db_profile.cidade,
                uf=db_profile.uf,
                telefone_fixo=db_profile.telefone_fixo,
                telefone_movel=db_profile.telefone_movel,
                whatsapp=db_profile.whatsapp,
                created_at=db_profile.created_at,
                updated_at=db_profile.updated_at
            )
            for db_profile in db_profiles
        ]

    def update(self, profile: Profile) -> Profile:
        """Atualizar profile"""
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.id == profile.id).first()
        if not db_profile:
            raise ValueError("Profile não encontrado")
        
        if profile.user_id is not None:
            db_profile.user_id = profile.user_id
        db_profile.role_id = profile.role_id
        db_profile.full_name = profile.full_name
        db_profile.artistic_name = profile.artistic_name
        db_profile.bio = profile.bio
        db_profile.cep = profile.cep
        db_profile.logradouro = profile.logradouro
        db_profile.numero = profile.numero
        db_profile.complemento = profile.complemento
        db_profile.cidade = profile.cidade
        db_profile.uf = profile.uf
        db_profile.telefone_fixo = profile.telefone_fixo
        db_profile.telefone_movel = profile.telefone_movel
        db_profile.whatsapp = profile.whatsapp
        db_profile.updated_at = profile.updated_at
        
        self.session.commit()
        self.session.refresh(db_profile)
        
        return Profile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            role_id=db_profile.role_id,
            full_name=db_profile.full_name,
            artistic_name=db_profile.artistic_name,
            bio=db_profile.bio,
            cep=db_profile.cep,
            logradouro=db_profile.logradouro,
            numero=db_profile.numero,
            complemento=db_profile.complemento,
            cidade=db_profile.cidade,
            uf=db_profile.uf,
            telefone_fixo=db_profile.telefone_fixo,
            telefone_movel=db_profile.telefone_movel,
            whatsapp=db_profile.whatsapp,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )

    def delete(self, profile_id: int) -> bool:
        """Deletar profile por ID"""
        db_profile = self.session.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not db_profile:
            return False
        
        self.session.delete(db_profile)
        self.session.commit()
        return True 