from datetime import datetime, timedelta, timezone

from db.database import SessionLocal
from core.security import hash_password
from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_task import CampaignTaskModel

def seed_data():
    db = SessionLocal()

    try:
        if db.query(UserModel).first():
            print("Database đã có dữ liệu, bỏ qua seed.")
            return

        admin = UserModel(
            email="admin@example.com",
            password_hash=hash_password("123456"),
            full_name="Admin User",
            role="ADMIN",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )

        user1 = UserModel(
            email="user1@example.com",
            password_hash=hash_password("123456"),
            full_name="Nguyen Van A",
            role="USER",
            is_active=True,
            created_at=datetime.now()
        )

        user2 = UserModel(
            email="user2@example.com",
            password_hash=hash_password("123456"),
            full_name="Tran Van B",
            role="USER",
            is_active=True,
            created_at=datetime.now()
        )

        db.add_all([admin, user1, user2])
        db.flush()

        campaign = CampaignModel(
            name="Summer Marketing 2026",
            description="Chiến dịch marketing mùa hè 2026",
            owner_id=admin.id,
            created_at=datetime.now()
        )

        db.add(campaign)
        db.flush()

        members = [
            CampaignMemberModel(
                campaign_id=campaign.id,
                user_id=admin.id,
                role="OWNER",
                joined_at=datetime.now()
            ),
            CampaignMemberModel(
                campaign_id=campaign.id,
                user_id=user1.id,
                role="MEMBER",
                joined_at=datetime.now()
            ),
            CampaignMemberModel(
                campaign_id=campaign.id,
                user_id=user2.id,
                role="MEMBER",
                joined_at=datetime.now()
            )
        ]

        db.add_all(members)

        tasks = [
            CampaignTaskModel(
                campaign_id=campaign.id,
                title="Thiết kế banner",
                description="Thiết kế banner cho chiến dịch",
                assignee_id=user1.id,
                status="TODO",
                priority="HIGH",
                due_date=datetime.now() + timedelta(days=3),
                created_at=datetime.now()
            ),
            CampaignTaskModel(
                campaign_id=campaign.id,
                title="Viết nội dung",
                description="Viết nội dung quảng cáo",
                assignee_id=user2.id,
                status="IN_PROGRESS",
                priority="MEDIUM",
                due_date=datetime.now() + timedelta(days=5),
                created_at=datetime.now()
            )
        ]

        db.add_all(tasks)

        db.commit()

        print("Thêm dữ liệu thành công")

    except Exception as e:
        db.rollback()
        print("Thêm thất bại")

    finally:
        db.close()

seed_data()