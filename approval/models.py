from django.db import models
from django.urls import reverse

from django.utils.translation import ugettext as _

from django.contrib.auth import get_user_model
# Create your models here.

class Identity(models.Model):

    name = models.CharField(_("SG ID"), max_length=50)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)

    class Meta:
        verbose_name = _("identity")
        verbose_name_plural = _("identitys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("identity_detail", kwargs={"pk": self.pk})

class Department(models.Model):

    name = models.CharField(_("Department Name"), max_length=50)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department_detail", kwargs={"pk": self.pk})



class ApprovalRequest(models.Model):

    sgid = models.ForeignKey("approval.Identity", verbose_name=_("SG ID"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=70)
    department = models.CharField(_("Department"), max_length=70)
    department_which = models.ForeignKey("approval.Department", verbose_name=_("Improve department in which"), on_delete=models.CASCADE)
    imporove = models.TextField(_("Improve Constant"))
    before_image = models.ImageField(_("Before Image"), upload_to="before_image")
    after_image = models.ImageField(_("After Image"), upload_to="after_image")

    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)
    

    class Meta:
        verbose_name = _("request")
        verbose_name_plural = _("requests")

    def __str__(self):
        return self.name

    @property
    def is_first_approved(self):
        approved = ApprovalOne.objects.filter(app_request=self, status=True).exists()
        if approved:
            return True
        return False

    @property
    def first_approval(self):
        return ApprovalOne.objects.filter(app_request=self, status=True).first()

    @property
    def second_approval(self):
        return ApprovalTwo.objects.filter(app_request=self, status=True).first()

    @property
    def is_second_approved(self):
        approved = ApprovalTwo.objects.filter(app_request=self, status=True).exists()
        if approved:
            return True
        return False

    def get_absolute_url(self):
        return reverse("request_detail", kwargs={"pk": self.pk})

class ApprovalOne(models.Model):

    app_request = models.ForeignKey("approval.ApprovalRequest", related_name='request_a1', verbose_name=_("Approval Request"), on_delete=models.CASCADE)
    status = models.BooleanField(_("Approve"), default=False)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    
    get_user_model()

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)

    class Meta:
        verbose_name = _("approval")
        verbose_name_plural = _("approvals")
        permissions = (
            ("level_one_approval", "Level One Approval"),
        )
    def __str__(self):
        return self.app_request.name

    def get_absolute_url(self):
        return reverse("approval_one_detail", kwargs={"pk": self.pk})


class ApprovalTwo(models.Model):

    app_request = models.ForeignKey("approval.ApprovalRequest", related_name='request_a2', verbose_name=_("Approval Two Request"), on_delete=models.CASCADE)
    status = models.BooleanField(_("Approve"), default=False)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)

    class Meta:
        verbose_name = _("approval")
        verbose_name_plural = _("approvals")
        permissions = (
            ("level_two_approval", "Level Two Approval"),
        )

    def __str__(self):
        return self.app_request.name

    def get_absolute_url(self):
        return reverse("approval_two_detail", kwargs={"pk": self.pk})


class Rejected(models.Model):

    app_request = models.ForeignKey("approval.ApprovalRequest", related_name='request_reject', verbose_name=_("Approval Two Request"), on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)
    

    class Meta:
        verbose_name = _("rejected")
        verbose_name_plural = _("rejecteds")

    def __str__(self):
        return self.app_request.name

    def get_absolute_url(self):
        return reverse("rejected_detail", kwargs={"pk": self.pk})


class Report(models.Model):

    app_request = models.ForeignKey("approval.ApprovalRequest", on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now=True)
    udpated = models.DateTimeField(_("Updated"), auto_now_add=True)

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")

    def __str__(self):
        return self.app_request.name

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"pk": self.pk})
        