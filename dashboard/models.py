from django.db import models


class VpsServer(models.Model):
    """
    One row per VPS (IONOS or other provider).
    Designed to be flexible and re-usable across the site.
    """

    PROVIDER_CHOICES = [
        ("IONOS", "IONOS"),
        ("OTHER", "Other"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Short ID / label, e.g. DS1-VPS-XS, DS2-VPS-S",
    )
    friendly_name = models.CharField(
        max_length=100,
        help_text="Human-readable name, e.g. cesserver1 / DS1 Main VPS",
    )
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default="IONOS",
    )
    package = models.CharField(
        max_length=100,
        blank=True,
        help_text="IONOS package type, e.g. VPS-XS / VPS-S / VPS-M",
    )

    main_ip = models.GenericIPAddressField(
        protocol="IPv4",
        null=True,
        blank=True,
        help_text="Primary public IP for the VPS.",
    )
    hostname = models.CharField(
        max_length=255,
        blank=True,
        help_text="System hostname, e.g. mail.cesserver1.com",
    )
    domain = models.CharField(
        max_length=255,
        blank=True,
        help_text="Primary domain attached, e.g. cesserver1.com",
    )

    webmail_url = models.URLField(blank=True)
    panel_url = models.URLField(blank=True, help_text="Hestia/Control panel URL")
    panel_username = models.CharField(max_length=150, blank=True)
    panel_password = models.CharField(
        max_length=255,
        blank=True,
        help_text="Consider moving secrets to a vault later.",
    )

    ssh_host = models.CharField(
        max_length=255,
        blank=True,
        help_text="SSH host, e.g. root@74.208.171.116",
    )
    ssh_user = models.CharField(max_length=100, blank=True, default="root")
    ssh_notes = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="Used in URLs, e.g. ds1-vps-xs",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.friendly_name}"
