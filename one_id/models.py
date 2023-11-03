from django.db import models


class OneIDProfile(models.Model):
    user = models.OneToOneField('auth.User', models.CASCADE, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    ctzn = models.CharField(max_length=255, blank=True, null=True)
    per_adr = models.CharField(max_length=255)
    tin = models.CharField(max_length=9, blank=True, null=True)
    pport_issue_place = models.CharField(max_length=255, blank=True, null=True)
    sur_name = models.CharField(max_length=255)
    gd = models.IntegerField(blank=True, null=True)
    natn = models.CharField(max_length=255, blank=True, null=True)
    pport_issue_date = models.DateField(blank=True, null=True)
    pport_expr_date = models.DateField(blank=True, null=True)
    pport_no = models.CharField(max_length=255)
    pin = models.CharField(max_length=14)
    mob_phone_no = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    mid_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=1)
    sess_id = models.CharField(max_length=255, blank=True, null=True)
    ret_cd = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class OneIDLegalInfo(models.Model):
    profile = models.ForeignKey(OneIDProfile, on_delete=models.CASCADE)
    le_tin = models.CharField(max_length=9)
    tin = models.CharField(max_length=9)
    legal_name = models.TextField()
    acron_uz = models.TextField()
    is_basic = models.BooleanField(default=False)

    def __str__(self):
        return self.legal_name


class OneIDToken(models.Model):
    profile = models.ForeignKey(OneIDProfile, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.DateTimeField()
