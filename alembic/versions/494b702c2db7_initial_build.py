"""initial build

Revision ID: 494b702c2db7
Revises:
Create Date: 2025-02-02 17:50:14.957838

"""

import sqlalchemy as sa
from sqlalchemy_utils.types.encrypted.encrypted_type import StringEncryptedType
from sqlalchemy_utils.types.ip_address import IPAddressType
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.uuid import UUIDType

from alembic import op
from app.db.custom_types import LongText, Scopes

# revision identifiers, used by Alembic.
revision = "494b702c2db7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organization",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_organization_id"), "organization", ["id"], unique=True)
    op.create_index(op.f("ix_organization_slug"), "organization", ["slug"], unique=True)
    op.create_index(op.f("ix_organization_title"), "organization", ["title"], unique=True)
    op.create_table(
        "geocoord",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("address", sa.String(length=704), nullable=False),
        sa.Column("latitude", sa.Float(precision=20), nullable=False),
        sa.Column("longitude", sa.Float(precision=20), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("address"),
        sa.UniqueConstraint("address"),
        sa.UniqueConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_table(
        "platform",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_platform_id"), "platform", ["id"], unique=True)
    op.create_index(op.f("ix_platform_slug"), "platform", ["slug"], unique=True)
    op.create_index(op.f("ix_platform_title"), "platform", ["title"], unique=True)
    op.create_table(
        "user",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("auth_id", StringEncryptedType(length=704), nullable=False),
        sa.Column("email", StringEncryptedType(length=1752), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("picture", StringEncryptedType(length=1752), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", StringEncryptedType(length=428), nullable=False),
        sa.Column("scopes", Scopes(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("auth_id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=True)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "website",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("domain", sa.String(length=704), nullable=False),
        sa.Column("is_secure", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("domain"),
        sa.UniqueConstraint("domain"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_website_id"), "website", ["id"], unique=True)
    op.create_table(
        "organization_platform",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("organization_id", "platform_id"),
    )
    op.create_index(
        op.f("ix_organization_platform_id"), "organization_platform", ["id"], unique=True
    )
    op.create_table(
        "organization_styleguide",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("styleguide", JSONType(), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_organization_styleguide_id"), "organization_styleguide", ["id"], unique=True
    )
    op.create_index(
        op.f("ix_organization_styleguide_title"), "organization_styleguide", ["title"], unique=True
    )
    op.create_table(
        "organization_website",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("organization_id", "website_id"),
    )
    op.create_index(op.f("ix_organization_website_id"), "organization_website", ["id"], unique=True)
    op.create_table(
        "gcft",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("group_name", sa.String(length=255), nullable=False),
        sa.Column("group_slug", sa.String(length=16), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_gcft_group_name"), "gcft", ["group_name"], unique=False)
    op.create_index(op.f("ix_gcft_group_slug"), "gcft", ["group_slug"], unique=False)
    op.create_index(op.f("ix_gcft_id"), "gcft", ["id"], unique=True)
    op.create_table(
        "go_a4",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("property_id", sa.String(length=16), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_go_a4_id"), "go_a4", ["id"], unique=True)
    op.create_index(op.f("ix_go_a4_property_id"), "go_a4", ["property_id"], unique=True)
    op.create_index(op.f("ix_go_a4_title"), "go_a4", ["title"], unique=True)
    op.create_table(
        "go_ads",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("measurement_id", sa.String(length=16), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_go_ads_id"), "go_ads", ["id"], unique=True)
    op.create_index(
        op.f("ix_go_ads_measurement_id"), "go_ads", ["measurement_id"], unique=True
    )
    op.create_index(op.f("ix_go_ads_title"), "go_ads", ["title"], unique=True)
    op.create_table(
        "go_sc",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_go_sc_id"), "go_sc", ["id"], unique=True)
    op.create_index(op.f("ix_go_sc_title"), "go_sc", ["title"], unique=True)
    op.create_table(
        "ipaddress",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("address", IPAddressType(length=50), nullable=False),
        sa.Column("hostname", sa.String(length=255), nullable=True),
        sa.Column("is_anycast", sa.Boolean(), nullable=True),
        sa.Column("city", sa.String(length=255), nullable=True),
        sa.Column("region", sa.String(length=255), nullable=True),
        sa.Column("country", sa.String(length=16), nullable=True),
        sa.Column("loc", sa.String(length=32), nullable=True),
        sa.Column("org", sa.String(length=255), nullable=True),
        sa.Column("postal", sa.String(length=16), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=True),
        sa.Column("country_name", sa.String(length=255), nullable=True),
        sa.Column("is_eu", sa.Boolean(), nullable=True),
        sa.Column("country_flag_url", sa.String(length=2048), nullable=True),
        sa.Column("country_flag_unicode", sa.String(length=2048), nullable=True),
        sa.Column("country_currency_code", sa.String(length=16), nullable=True),
        sa.Column("continent_code", sa.String(length=16), nullable=True),
        sa.Column("continent_name", sa.String(length=16), nullable=True),
        sa.Column("latitude", sa.String(length=16), nullable=True),
        sa.Column("longitude", sa.String(length=16), nullable=True),
        sa.Column("geocoord_id", UUIDType(binary=False), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["geocoord_id"],
            ["geocoord.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_ipaddress_address"), "ipaddress", ["address"], unique=True)
    op.create_index(op.f("ix_ipaddress_id"), "ipaddress", ["id"], unique=True)
    op.create_table(
        "tracking_link",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("url_hash", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("scheme", sa.String(length=16), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("destination", sa.String(length=2048), nullable=False),
        sa.Column("url_path", sa.String(length=2048), nullable=False),
        sa.Column("utm_campaign", sa.String(length=255), nullable=True),
        sa.Column("utm_medium", sa.String(length=255), nullable=True),
        sa.Column("utm_source", sa.String(length=255), nullable=True),
        sa.Column("utm_content", sa.String(length=255), nullable=True),
        sa.Column("utm_term", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url_hash"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_tracking_link_id"), "tracking_link", ["id"], unique=True)
    op.create_table(
        "user_organization",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("user_id", UUIDType(binary=False), nullable=False),
        sa.Column("organization_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "organization_id"),
    )
    op.create_index(op.f("ix_user_organization_id"), "user_organization", ["id"], unique=True)
    op.create_table(
        "website_page",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.Column("priority", sa.Float(), nullable=False),
        sa.Column("last_modified", sa.DateTime(timezone=True), nullable=True),
        sa.Column("change_frequency", sa.String(length=704), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_website_page_id"), "website_page", ["id"], unique=True)
    op.create_index(
        op.f("ix_website_page_website_id"), "website_page", ["website_id"], unique=False
    )
    op.create_table(
        "gcft_snap",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_name", sa.String(length=255), nullable=False),
        sa.Column("snap_slug", sa.String(length=16), nullable=False),
        sa.Column("altitude", sa.Integer(), nullable=False),
        sa.Column("geocoord_id", UUIDType(binary=False), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["geocoord_id"],
            ["geocoord.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_gcft_snap_id"), "gcft_snap", ["id"], unique=True)
    op.create_index(
        op.f("ix_gcft_snap_snap_name"), "gcft_snap", ["snap_name"], unique=False
    )
    op.create_index(
        op.f("ix_gcft_snap_snap_slug"), "gcft_snap", ["snap_slug"], unique=True
    )
    op.create_table(
        "go_a4_stream",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("stream_id", sa.String(length=16), nullable=False),
        sa.Column("measurement_id", sa.String(length=16), nullable=False),
        sa.Column("ga4_id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ga4_id"],
            ["go_a4.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_go_a4_stream_id"), "go_a4_stream", ["id"], unique=True)
    op.create_index(
        op.f("ix_go_a4_stream_measurement_id"),
        "go_a4_stream",
        ["measurement_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_go_a4_stream_stream_id"), "go_a4_stream", ["stream_id"], unique=True
    )
    op.create_index(
        op.f("ix_go_a4_stream_title"), "go_a4_stream", ["title"], unique=True
    )
    op.create_table(
        "user_ipaddress",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("user_id", UUIDType(binary=False), nullable=False),
        sa.Column("ipaddress_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ipaddress_id"],
            ["ipaddress.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "ipaddress_id"),
    )
    op.create_index(op.f("ix_user_ipaddress_id"), "user_ipaddress", ["id"], unique=True)
    op.create_table(
        "website_go_a4",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("go_a4_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["go_a4_id"],
            ["go_a4.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("website_id", "go_a4_id"),
    )
    op.create_index(op.f("ix_website_go_a4_id"), "website_go_a4", ["id"], unique=True)
    op.create_table(
        "website_go_ads",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("go_ads_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["go_ads_id"],
            ["go_ads.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("website_id", "go_ads_id"),
    )
    op.create_index(op.f("ix_website_go_ads_id"), "website_go_ads", ["id"], unique=True)
    op.create_table(
        "website_keywordcorpus",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("corpus", LongText(), nullable=False),
        sa.Column("rawtext", LongText(), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("page_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["page_id"],
            ["website_page.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_website_keywordcorpus_id"),
        "website_keywordcorpus",
        ["id"],
        unique=True,
    )
    op.create_table(
        "website_pagespeedinsights",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("strategy", sa.String(length=408), nullable=False),
        sa.Column("score_grade", sa.Float(), nullable=False),
        sa.Column("grade_data", JSONType(), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("page_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["page_id"],
            ["website_page.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_website_pagespeedinsights_id"),
        "website_pagespeedinsights",
        ["id"],
        unique=True,
    )
    op.create_table(
        "gcft_snap_activeduration",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("session_id", UUIDType(binary=False), nullable=False),
        sa.Column("active_seconds", sa.INTEGER(), nullable=False),
        sa.Column("visit_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["snap_id"],
            ["gcft_snap.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_gcft_snap_activeduration_id"),
        "gcft_snap_activeduration",
        ["id"],
        unique=True,
    )
    op.create_table(
        "gcft_snap_browserreport",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("session_id", UUIDType(binary=False), nullable=False),
        sa.Column("browser", sa.String(length=704), nullable=True),
        sa.Column("browser_version", sa.String(length=704), nullable=True),
        sa.Column("platform", sa.String(length=704), nullable=True),
        sa.Column("platform_version", sa.String(length=704), nullable=True),
        sa.Column("desktop", sa.Boolean(), nullable=True),
        sa.Column("tablet", sa.Boolean(), nullable=True),
        sa.Column("mobile", sa.Boolean(), nullable=True),
        sa.Column("city", sa.String(length=704), nullable=True),
        sa.Column("country", sa.String(length=704), nullable=True),
        sa.Column("state", sa.String(length=704), nullable=True),
        sa.Column("language", sa.String(length=704), nullable=True),
        sa.Column("visit_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["snap_id"],
            ["gcft_snap.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_gcft_snap_browserreport_id"),
        "gcft_snap_browserreport",
        ["id"],
        unique=True,
    )
    op.create_table(
        "gcft_snap_hotspotclick",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("session_id", UUIDType(binary=False), nullable=False),
        sa.Column("reporting_id", sa.String(length=428), nullable=True),
        sa.Column("hotspot_type_name", sa.String(length=428), nullable=True),
        sa.Column("hotspot_content", LongText(), nullable=True),
        sa.Column("hotspot_icon_name", sa.String(length=704), nullable=True),
        sa.Column("hotspot_name", sa.String(length=704), nullable=True),
        sa.Column("hotspot_user_icon_name", sa.String(length=704), nullable=True),
        sa.Column("linked_snap_name", sa.String(length=704), nullable=True),
        sa.Column("snap_file_name", sa.String(length=704), nullable=True),
        sa.Column("icon_color", sa.String(length=428), nullable=True),
        sa.Column("bg_color", sa.String(length=428), nullable=True),
        sa.Column("text_color", sa.String(length=428), nullable=True),
        sa.Column("hotspot_update_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("click_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["snap_id"],
            ["gcft_snap.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_gcft_snap_hotspotclick_id"),
        "gcft_snap_hotspotclick",
        ["id"],
        unique=True,
    )
    op.create_table(
        "gcft_snap_trafficsource",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("session_id", UUIDType(binary=False), nullable=False),
        sa.Column("referrer", sa.String(length=3116), nullable=False),
        sa.Column("utm_campaign", sa.String(length=704), nullable=True),
        sa.Column("utm_content", sa.String(length=704), nullable=True),
        sa.Column("utm_medium", sa.String(length=704), nullable=True),
        sa.Column("utm_source", sa.String(length=704), nullable=True),
        sa.Column("utm_term", sa.String(length=704), nullable=True),
        sa.Column("visit_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["snap_id"],
            ["gcft_snap.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_gcft_snap_trafficsource_id"),
        "gcft_snap_trafficsource",
        ["id"],
        unique=True,
    )
    op.create_table(
        "gcft_snap_view",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("session_id", UUIDType(binary=False), nullable=False),
        sa.Column("view_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("gcft_id", UUIDType(binary=False), nullable=False),
        sa.Column("snap_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gcft_id"],
            ["gcft.id"],
        ),
        sa.ForeignKeyConstraint(
            ["snap_id"],
            ["gcft_snap.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_gcft_snap_view_id"), "gcft_snap_view", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_gcft_snap_view_id"), table_name="gcft_snap_view")
    op.drop_table("gcft_snap_view")
    op.drop_index(
        op.f("ix_gcft_snap_trafficsource_id"), table_name="gcft_snap_trafficsource"
    )
    op.drop_table("gcft_snap_trafficsource")
    op.drop_index(
        op.f("ix_gcft_snap_hotspotclick_id"), table_name="gcft_snap_hotspotclick"
    )
    op.drop_table("gcft_snap_hotspotclick")
    op.drop_index(
        op.f("ix_gcft_snap_browserreport_id"), table_name="gcft_snap_browserreport"
    )
    op.drop_table("gcft_snap_browserreport")
    op.drop_index(
        op.f("ix_gcft_snap_activeduration_id"), table_name="gcft_snap_activeduration"
    )
    op.drop_table("gcft_snap_activeduration")
    op.drop_index(
        op.f("ix_website_pagespeedinsights_id"), table_name="website_pagespeedinsights"
    )
    op.drop_table("website_pagespeedinsights")
    op.drop_index(
        op.f("ix_website_keywordcorpus_id"), table_name="website_keywordcorpus"
    )
    op.drop_table("website_keywordcorpus")
    op.drop_index(op.f("ix_website_go_ads_id"), table_name="website_go_ads")
    op.drop_table("website_go_ads")
    op.drop_index(op.f("ix_website_go_a4_id"), table_name="website_go_a4")
    op.drop_table("website_go_a4")
    op.drop_index(op.f("ix_user_ipaddress_id"), table_name="user_ipaddress")
    op.drop_table("user_ipaddress")
    op.drop_index(op.f("ix_go_a4_stream_title"), table_name="go_a4_stream")
    op.drop_index(op.f("ix_go_a4_stream_stream_id"), table_name="go_a4_stream")
    op.drop_index(op.f("ix_go_a4_stream_measurement_id"), table_name="go_a4_stream")
    op.drop_index(op.f("ix_go_a4_stream_id"), table_name="go_a4_stream")
    op.drop_table("go_a4_stream")
    op.drop_index(op.f("ix_gcft_snap_snap_slug"), table_name="gcft_snap")
    op.drop_index(op.f("ix_gcft_snap_snap_name"), table_name="gcft_snap")
    op.drop_index(op.f("ix_gcft_snap_id"), table_name="gcft_snap")
    op.drop_table("gcft_snap")
    op.drop_index(op.f("ix_website_page_website_id"), table_name="website_page")
    op.drop_index(op.f("ix_website_page_id"), table_name="website_page")
    op.drop_table("website_page")
    op.drop_index(op.f("ix_user_organization_id"), table_name="user_organization")
    op.drop_table("user_organization")
    op.drop_index(op.f("ix_tracking_link_id"), table_name="tracking_link")
    op.drop_table("tracking_link")
    op.drop_index(op.f("ix_ipaddress_id"), table_name="ipaddress")
    op.drop_index(op.f("ix_ipaddress_address"), table_name="ipaddress")
    op.drop_table("ipaddress")
    op.drop_index(op.f("ix_go_sc_title"), table_name="go_sc")
    op.drop_index(op.f("ix_go_sc_id"), table_name="go_sc")
    op.drop_table("go_sc")
    op.drop_index(op.f("ix_go_ads_title"), table_name="go_ads")
    op.drop_index(op.f("ix_go_ads_measurement_id"), table_name="go_ads")
    op.drop_index(op.f("ix_go_ads_id"), table_name="go_ads")
    op.drop_table("go_ads")
    op.drop_index(op.f("ix_go_a4_title"), table_name="go_a4")
    op.drop_index(op.f("ix_go_a4_property_id"), table_name="go_a4")
    op.drop_index(op.f("ix_go_a4_id"), table_name="go_a4")
    op.drop_table("go_a4")
    op.drop_index(op.f("ix_gcft_id"), table_name="gcft")
    op.drop_index(op.f("ix_gcft_group_slug"), table_name="gcft")
    op.drop_index(op.f("ix_gcft_group_name"), table_name="gcft")
    op.drop_table("gcft")
    op.drop_index(op.f("ix_organization_website_id"), table_name="organization_website")
    op.drop_table("organization_website")
    op.drop_index(op.f("ix_organization_styleguide_title"), table_name="organization_styleguide")
    op.drop_index(op.f("ix_organization_styleguide_id"), table_name="organization_styleguide")
    op.drop_table("organization_styleguide")
    op.drop_index(op.f("ix_organization_platform_id"), table_name="organization_platform")
    op.drop_table("organization_platform")
    op.drop_index(op.f("ix_website_id"), table_name="website")
    op.drop_table("website")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_platform_title"), table_name="platform")
    op.drop_index(op.f("ix_platform_slug"), table_name="platform")
    op.drop_index(op.f("ix_platform_id"), table_name="platform")
    op.drop_table("platform")
    op.drop_table("geocoord")
    op.drop_index(op.f("ix_organization_title"), table_name="organization")
    op.drop_index(op.f("ix_organization_slug"), table_name="organization")
    op.drop_index(op.f("ix_organization_id"), table_name="organization")
    op.drop_table("organization")
    # ### end Alembic commands ###
