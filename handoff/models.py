from django.db import models


class AgentTiming(models.Model):
    id = models.BigAutoField(primary_key=True)
    working_day = models.CharField(unique=True, max_length=1)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        managed = False
        db_table = "agent_timing"


class AnalyticsSocialevent(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=200)
    event = models.CharField(max_length=200)
    session = models.CharField(max_length=36)
    timestamp = models.DateTimeField()
    channel = models.CharField(max_length=100, blank=True, null=True)
    agent = models.ForeignKey(
        "SocialconversationAgent", models.DO_NOTHING, blank=True, null=True
    )
    social = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING, blank=True, null=True
    )
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)
    bot_session_id = models.CharField(max_length=200, blank=True, null=True)
    parent_session_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = "analytics_socialevent"


class ChatMessagesocialagent(models.Model):
    socialplatformmixin_ptr = models.OneToOneField(
        "SocialconversationSocialplatformmixin", models.DO_NOTHING, primary_key=True
    )
    sender = models.CharField(max_length=13)
    body = models.TextField()
    sentiment = models.CharField(max_length=100)
    message_type = models.CharField(max_length=100)
    intent = models.CharField(max_length=200, blank=True, null=True)
    session_key = models.CharField(max_length=36, blank=True, null=True)
    chat_user = models.ForeignKey(
        "SocialconversationAgent", models.DO_NOTHING, blank=True, null=True
    )
    social_user = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING, blank=True, null=True
    )
    tenant = models.CharField(max_length=201, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_messagesocialagent"


class ChatSocialagentsession(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_key = models.CharField(max_length=36, blank=True, null=True)
    chat_user = models.ForeignKey(
        "SocialconversationAgent", models.DO_NOTHING, blank=True, null=True
    )
    social_user = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "chat_socialagentsession"


class SocialconversationAgent(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(unique=True, max_length=199)
    max_concurrent = models.IntegerField()
    current_chats = models.IntegerField()
    is_online = models.BooleanField()
    is_ready = models.BooleanField()
    username = models.CharField(max_length=199)

    class Meta:
        managed = False
        db_table = "socialconversation_agent"


class SocialconversationAgentsecondaryskill(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(SocialconversationAgent, models.DO_NOTHING)
    skill = models.ForeignKey("SocialconversationSkill", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "socialconversation_agentsecondaryskill"


class SocialconversationAgentskill(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(SocialconversationAgent, models.DO_NOTHING)
    skill = models.ForeignKey("SocialconversationSkill", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "socialconversation_agentskill"


class SocialconversationAgenttenant(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(SocialconversationAgent, models.DO_NOTHING)
    tenant = models.ForeignKey("SocialconversationTenant", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "socialconversation_agenttenant"


class SocialconversationAttributes(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = "socialconversation_attributes"


class SocialconversationCannedresponses(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(unique=True, max_length=50)
    text = models.CharField(max_length=499)

    class Meta:
        managed = False
        db_table = "socialconversation_cannedresponses"


class SocialconversationDirectMessage(models.Model):
    socialplatformmixin_ptr = models.OneToOneField(
        "SocialconversationSocialplatformmixin", models.DO_NOTHING, primary_key=True
    )
    body = models.CharField(max_length=100, blank=True, null=True)
    sentiment = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=50)
    sender = models.CharField(max_length=255)
    receiver = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING, related_name="receiver"
    )
    user = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING, related_name="user"
    )

    class Meta:
        managed = False
        db_table = "socialconversation_direct_message"


class SocialconversationSentiment(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentiment_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "socialconversation_sentiment"


class SocialconversationSentimentrelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentiment = models.ForeignKey(SocialconversationSentiment, models.DO_NOTHING)
    direct_message = models.ForeignKey(
        SocialconversationDirectMessage, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "socialconversation_sentimentrelation"


class SocialconversationSkill(models.Model):
    id = models.BigAutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "socialconversation_skill"


class SocialconversationSocialplatformmixin(models.Model):
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "socialconversation_socialplatformmixin"


class SocialconversationSocialusernotes(models.Model):
    socialplatformmixin_ptr = models.OneToOneField(
        SocialconversationSocialplatformmixin, models.DO_NOTHING, primary_key=True
    )
    note = models.CharField(max_length=150)
    social_user = models.ForeignKey(
        "SocialconversationTempsocialuser", models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "socialconversation_socialusernotes"


class SocialconversationTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = "socialconversation_tag"


class SocialconversationTagsocialmessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    social_message = models.ForeignKey(
        SocialconversationSocialplatformmixin, models.DO_NOTHING
    )
    tag = models.ForeignKey(SocialconversationTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "socialconversation_tagsocialmessage"


class SocialconversationTempsocialuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=200)
    channel_id = models.CharField(max_length=200)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    channel = models.CharField(max_length=50, blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)
    last_activity = models.DateTimeField()
    is_circulating = models.BooleanField()
    agent = models.ForeignKey(
        SocialconversationAgent, models.DO_NOTHING, blank=True, null=True
    )
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "socialconversation_tempsocialuser"


class SocialconversationTempsocialuserattribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute = models.ForeignKey(
        SocialconversationAttributes, models.DO_NOTHING, blank=True, null=True
    )
    social_user = models.ForeignKey(SocialconversationTempsocialuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "socialconversation_tempsocialuserattribute"


class SocialconversationTenant(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "socialconversation_tenant"


class NewUserInHandoff(models.Model):
    social_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=200)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "new_user_in_handoff"


class ReturningUserInHandoff(models.Model):
    social_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)
    return_time = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=200)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "returning_user_in_handoff"


class Handoffduration(models.Model):
    username = models.CharField(max_length=199, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    session = models.CharField(max_length=36, blank=True, null=True)
    minutes = models.FloatField(blank=True, null=True)
    agent_id = models.BigIntegerField(blank=True, null=True)
    social_id = models.BigIntegerField(blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "handoffduration"


class AbandonedDetails(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    session = models.CharField(max_length=36, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    social_id = models.BigIntegerField(blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    event = models.CharField(max_length=200, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "abandoned_details"


class AgentLastActivityTime(models.Model):
    dt = models.DateField(blank=True, null=True)
    diff = models.DateTimeField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(max_length=199, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "agent_last_activity_time"


class AgentSkill(models.Model):
    agent_id = models.BigIntegerField(blank=True, null=True)
    skill_id = models.BigIntegerField(blank=True, null=True)
    skill_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=199, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "agent_skill"


class CurrentLoggedIn(models.Model):
    agent_id = models.BigIntegerField(blank=True, null=True)
    skill_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=199, blank=True, null=True)
    is_online = models.BooleanField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True, blank=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "current_logged_in"


class AuditlogLogentry(models.Model):
    object_pk = models.CharField(max_length=255)
    object_id = models.BigIntegerField(blank=True, null=True)
    object_repr = models.TextField()
    action = models.SmallIntegerField()
    changes = models.TextField()
    timestamp = models.DateTimeField()
    actor = models.ForeignKey("AuthUser", models.DO_NOTHING, blank=True, null=True)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    serialized_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "auditlog_logentry"


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class AgentProductivity(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    agent_routed = models.TextField(
        blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    session_id = models.CharField(max_length=36, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    agent_accept = models.TextField(
        blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    accept_time = models.DurationField(
        blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters.
    initial_time = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "agent_productivity"


class AgentTransfer(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    parent_session_id = models.CharField(max_length=36, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    transferred_agents = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    initial_agent = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    total_session = models.DurationField(blank=True, null=True)
    initial_time = models.DateTimeField(blank=True, null=True)
    accept_time = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "agent_transfer"


class HandoffFlow(models.Model):
    session_id = models.CharField(max_length=36, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    target = models.CharField(max_length=200, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "handoff_flow"
