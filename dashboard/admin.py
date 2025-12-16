import csv
import io

from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.text import slugify

from .models import VpsServer
from .forms import VpsCsvImportForm


@admin.register(VpsServer)
class VpsServerAdmin(admin.ModelAdmin):
    list_display = ("code", "friendly_name", "provider", "package", "main_ip", "is_active")
    list_filter = ("provider", "is_active", "package")
    search_fields = ("code", "friendly_name", "main_ip", "hostname", "domain")
    prepopulated_fields = {"slug": ("code",)}

    # NOTE: This expects templates at:
    # templates/admin/dashboard/vpsserver/change_list.html
    # templates/admin/dashboard/vpsserver/import_csv.html
    change_list_template = "admin/dashboard/vpsserver/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv),
                name="dashboard_vpsserver_import_csv",
            ),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        """
        Admin page that imports VPS servers from a CSV file.

        Requirements:
        - CSV should include a column named: code
          (we also tolerate Code/CODE and BOM-prefixed headers)
        """
        if request.method == "POST":
            form = VpsCsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded = form.cleaned_data["csv_file"]

                # Read bytes and decode safely (handles UTF-8 w/ weird chars)
                data = uploaded.read().decode("utf-8", errors="replace")
                reader = csv.DictReader(io.StringIO(data))

                created = 0
                updated = 0
                skipped = 0
                warned_headers = False

                for row in reader:
                    # tolerate common header variations: code, Code, BOM, etc.
                    code = ""
                    for k in ("code", "Code", "CODE", "\ufeffcode", "\ufeffCode", "\ufeffCODE"):
                        if k in row and row[k]:
                            code = str(row[k]).strip()
                            break

                    if not code:
                        skipped += 1
                        if not warned_headers:
                            self.message_user(
                                request,
                                f"Some rows were skipped because 'code' was empty or the header didn't match. "
                                f"Headers seen: {list(row.keys())[:12]}",
                                level=messages.WARNING,
                            )
                            warned_headers = True
                        continue

                    defaults = {
                        "friendly_name": (row.get("friendly_name") or "").strip(),
                        "provider": (row.get("provider") or "IONOS").strip() or "IONOS",
                        "package": (row.get("package") or "").strip(),
                        "main_ip": (row.get("main_ip") or "").strip() or None,
                        "hostname": (row.get("hostname") or "").strip(),
                        "domain": (row.get("domain") or "").strip(),
                        "panel_url": (row.get("panel_url") or "").strip(),
                        "webmail_url": (row.get("webmail_url") or "").strip(),
                        "panel_username": (row.get("panel_username") or "").strip(),
                        "panel_password": (row.get("panel_password") or "").strip(),
                        "ssh_host": (row.get("ssh_host") or "").strip(),
                        "ssh_user": (row.get("ssh_user") or "").strip() or "root",
                        "notes": (row.get("notes") or "").strip(),
                    }

                    active_raw = (row.get("is_active") or "").strip().lower()
                    defaults["is_active"] = active_raw in ("1", "true", "yes", "y")

                    slug = (row.get("slug") or "").strip()
                    defaults["slug"] = slug or slugify(code)

                    obj, was_created = VpsServer.objects.update_or_create(
                        code=code,
                        defaults=defaults,
                    )

                    if was_created:
                        created += 1
                    else:
                        updated += 1

                self.message_user(
                    request,
                    f"Import complete: {created} created, {updated} updated, {skipped} skipped.",
                    level=messages.SUCCESS,
                )
                return redirect("..")

        else:
            form = VpsCsvImportForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "form": form,
            "title": "Import VPS Servers from CSV",
        }
        return render(request, "admin/dashboard/vpsserver/import_csv.html", context)
