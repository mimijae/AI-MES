from django.db import models
from users.models import User

from common.models import CommonModel  # User 모델 참조

class Organization(CommonModel):
    """조직 모델"""

    ORGANIZATION_TYPE_CHOICES = [
        ('club', 'Club'),
        ('lab', 'Lab'),
        ('student_council', 'Student Council'),
    ]

    name = models.CharField(max_length=100, unique=True)  # 조직명
    description = models.TextField(blank=True)  # 조직 설명
    organization_type = models.CharField(
        max_length=20,
        choices=ORGANIZATION_TYPE_CHOICES,
        default='club',
    )  # 조직 유형
    contact_email = models.EmailField(blank=True)  # 연락 이메일
    contact_phone = models.CharField(max_length=15, blank=True)  # 연락처
    address = models.CharField(max_length=255, blank=True)  # 주소
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organizations_created")  # 조직 생성자

    class Meta:
        db_table = 'organization'  # 테이블 이름을 'organization'으로 지정

    def __str__(self):
        return f"{self.name} ({self.get_organization_type_display()})"


class OrganizationMember(CommonModel):
    """조직 구성원 모델"""

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")  # 조직
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organization_memberships")  # 사용자
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')  # 역할

    class Meta:
        db_table = 'organization_member'  # 테이블 이름을 'organization_member'로 지정
        unique_together = ('organization', 'user')  # 같은 사용자가 동일한 조직에 중복 가입하지 않도록 제한

    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role})"
