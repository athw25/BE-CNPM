from typing import Optional, List
from sqlalchemy import select, func
from infrastructure.databases.db_base import SessionLocal as _SessionLocal
from infrastructure.models.recruitment_models import RecruitmentCampaign as CampaignORM, Application as AppORM
from domain.models.recruitment import RecruitmentCampaignDomain, ApplicationDomain

class CampaignRepository:
    def __init__(self, session_factory=None):
        self.SessionLocal = session_factory or _SessionLocal

    # ---- READ
    def get_by_id(self, camp_id: int) -> Optional[RecruitmentCampaignDomain]:
        with self.SessionLocal() as s:
            obj = s.get(CampaignORM, camp_id)
            return self._to_domain(obj) if obj else None

    def list(self, status: Optional[str] = None) -> List[RecruitmentCampaignDomain]:
        with self.SessionLocal() as s:
            stmt = select(CampaignORM).order_by(CampaignORM.campID.asc())
            if status:
                stmt = stmt.where(CampaignORM.status == status)
            return [self._to_domain(x) for x in s.execute(stmt).scalars().all()]

    def count_applications(self, camp_id: int) -> int:
        with self.SessionLocal() as s:
            cnt = s.execute(
                select(func.count()).select_from(AppORM).where(AppORM.campID == camp_id)
            ).scalar()
            return int(cnt or 0)

    # ---- WRITE
    def create(self, c: RecruitmentCampaignDomain) -> RecruitmentCampaignDomain:
        with self.SessionLocal() as s:
            obj = CampaignORM(title=c.title, status=c.status)
            s.add(obj)
            s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def update(self, c: RecruitmentCampaignDomain) -> Optional[RecruitmentCampaignDomain]:
        with self.SessionLocal() as s:
            obj = s.get(CampaignORM, c.campID)
            if not obj:
                return None
            obj.title  = c.title if c.title is not None else obj.title
            obj.status = c.status if c.status is not None else obj.status
            s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def delete(self, camp_id: int) -> bool:
        with self.SessionLocal() as s:
            obj = s.get(CampaignORM, camp_id)
            if not obj:
                return False
            s.delete(obj); s.commit()
            return True

    def _to_domain(self, o: CampaignORM) -> RecruitmentCampaignDomain:
        return RecruitmentCampaignDomain(campID=o.campID, title=o.title, status=o.status)


class ApplicationRepository:
    def __init__(self, session_factory=None):
        self.SessionLocal = session_factory or _SessionLocal

    # ---- READ
    def get_by_id(self, app_id: int) -> Optional[ApplicationDomain]:
        with self.SessionLocal() as s:
            obj = s.get(AppORM, app_id)
            return self._to_domain(obj) if obj else None

    def list(self, camp_id: Optional[int] = None, user_id: Optional[int] = None) -> List[ApplicationDomain]:
        with self.SessionLocal() as s:
            stmt = select(AppORM).order_by(AppORM.appID.asc())
            if camp_id is not None:
                stmt = stmt.where(AppORM.campID == camp_id)
            if user_id is not None:
                stmt = stmt.where(AppORM.userID == user_id)
            return [self._to_domain(x) for x in s.execute(stmt).scalars().all()]

    # ---- WRITE
    def create(self, a: ApplicationDomain) -> ApplicationDomain:
        with self.SessionLocal() as s:
            obj = AppORM(campID=a.campID, userID=a.userID, status=a.status)
            s.add(obj); s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def update(self, a: ApplicationDomain) -> Optional[ApplicationDomain]:
        with self.SessionLocal() as s:
            obj = s.get(AppORM, a.appID)
            if not obj:
                return None
            obj.status = a.status if a.status is not None else obj.status
            s.commit(); s.refresh(obj)
            return self._to_domain(obj)

    def delete(self, app_id: int) -> bool:
        with self.SessionLocal() as s:
            obj = s.get(AppORM, app_id)
            if not obj:
                return False
            s.delete(obj); s.commit()
            return True

    def _to_domain(self, o: AppORM) -> ApplicationDomain:
        return ApplicationDomain(appID=o.appID, campID=o.campID, userID=o.userID, status=o.status)
