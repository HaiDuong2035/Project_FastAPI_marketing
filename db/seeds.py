from datetime import datetime, timedelta, timezone

from db.database import SessionLocal
from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_task import CampaignTaskModel
from models.campaign_task_comment import CampaignTaskCommentModel
from models.campaign_log import CampaignLogModel

db = SessionLocal()

try:
    users = [
        UserModel(
            id=1,
            email="admin@gmail.com",
            password_hash="hashed_password_1",
            full_name="Admin User",
            role="ADMIN",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        ),
        UserModel(
            id=2,
            email="nguyenvana@gmail.com",
            password_hash="hashed_password_2",
            full_name="Nguyen Van A",
            role="USER",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        ),
        UserModel(
            id=3,
            email="tranthib@gmail.com",
            password_hash="hashed_password_3",
            full_name="Tran Thi B",
            role="USER",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        ),
        UserModel(
            id=4,
            email="levanc@gmail.com",
            password_hash="hashed_password_4",
            full_name="Le Van C",
            role="USER",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        ),
    ]

    db.add_all(users)
    db.flush()

    campaigns = [
        CampaignModel(
            id=1,
            name="Summer Marketing Campaign",
            description="Chiến dịch marketing mùa hè",
            owner_id=1,
            created_at=datetime.now(timezone.utc),
            is_delete=False,
        ),
        CampaignModel(
            id=2,
            name="Product Launch Campaign",
            description="Chiến dịch ra mắt sản phẩm mới",
            owner_id=2,
            created_at=datetime.now(timezone.utc),
            is_delete=False,
        ),
        CampaignModel(
            id=3,
            name="Social Media Campaign",
            description="Chiến dịch truyền thông mạng xã hội",
            owner_id=3,
            created_at=datetime.now(timezone.utc),
            is_delete=False,
        ),
    ]

    db.add_all(campaigns)
    db.flush()

    members = [
        CampaignMemberModel(
            campaign_id=1,
            user_id=1,
            role="OWNER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=1,
            user_id=2,
            role="MEMBER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=1,
            user_id=3,
            role="MEMBER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=2,
            user_id=2,
            role="OWNER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=2,
            user_id=4,
            role="MEMBER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=3,
            user_id=3,
            role="OWNER",
            joined_at=datetime.now(timezone.utc),
        ),
        CampaignMemberModel(
            campaign_id=3,
            user_id=4,
            role="MEMBER",
            joined_at=datetime.now(timezone.utc),
        ),
    ]

    db.add_all(members)
    db.flush()

    tasks = [
        CampaignTaskModel(
            id=1,
            campaign_id=1,
            title="Create marketing plan",
            description="Xây dựng kế hoạch marketing cho chiến dịch",
            assignee_id=2,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now(timezone.utc) + timedelta(days=7),
            created_at=datetime.now(timezone.utc),
            created_by_id=1,
        ),
        CampaignTaskModel(
            id=2,
            campaign_id=1,
            title="Design banner",
            description="Thiết kế banner quảng cáo",
            assignee_id=3,
            status="IN_PROGRESS",
            priority="MEDIUM",
            due_date=datetime.now(timezone.utc) + timedelta(days=5),
            created_at=datetime.now(timezone.utc),
            created_by_id=1,
        ),
        CampaignTaskModel(
            id=3,
            campaign_id=2,
            title="Prepare product demo",
            description="Chuẩn bị video demo sản phẩm",
            assignee_id=4,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now(timezone.utc) + timedelta(days=10),
            created_at=datetime.now(timezone.utc),
            created_by_id=2,
        ),
        CampaignTaskModel(
            id=4,
            campaign_id=3,
            title="Create social posts",
            description="Tạo nội dung cho mạng xã hội",
            assignee_id=4,
            status="DONE",
            priority="LOW",
            due_date=datetime.now(timezone.utc) - timedelta(days=1),
            created_at=datetime.now(timezone.utc),
            created_by_id=3,
        ),
    ]

    db.add_all(tasks)
    db.flush()

    comments = [
        CampaignTaskCommentModel(
            id=1,
            campaign_task_id=1,
            user_id=2,
            content="Tôi sẽ hoàn thành kế hoạch trong tuần này.",
            created_at=datetime.now(timezone.utc),
        ),
        CampaignTaskCommentModel(
            id=2,
            campaign_task_id=1,
            user_id=1,
            content="Hãy bổ sung thêm phần ngân sách.",
            created_at=datetime.now(timezone.utc),
        ),
        CampaignTaskCommentModel(
            id=3,
            campaign_task_id=2,
            user_id=3,
            content="Banner đã hoàn thành bản thiết kế đầu tiên.",
            created_at=datetime.now(timezone.utc),
        ),
        CampaignTaskCommentModel(
            id=4,
            campaign_task_id=3,
            user_id=4,
            content="Video demo đang được chuẩn bị.",
            created_at=datetime.now(timezone.utc),
        ),
    ]

    db.add_all(comments)
    db.flush()

    logs = [
        CampaignLogModel(
            id=1,
            campaign_id=1,
            user_id=1,
            activity="CREATE",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=2,
            campaign_id=1,
            user_id=2,
            activity="JOIN",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=3,
            campaign_id=1,
            user_id=3,
            activity="JOIN",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=4,
            campaign_id=2,
            user_id=2,
            activity="CREATE",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=5,
            campaign_id=2,
            user_id=4,
            activity="JOIN",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=6,
            campaign_id=3,
            user_id=3,
            activity="CREATE",
            did_at=datetime.now(timezone.utc),
        ),
        CampaignLogModel(
            id=7,
            campaign_id=3,
            user_id=4,
            activity="JOIN",
            did_at=datetime.now(timezone.utc),
        ),
    ]

    db.add_all(logs)

    db.commit()

    print("Seed data successfully!")

except Exception as e:
    db.rollback()
    print(f"Seed failed: {e}")

finally:
    db.close()