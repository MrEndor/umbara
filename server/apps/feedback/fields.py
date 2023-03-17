from server.apps.feedback import models

FeedbackTextField: str = (
    models.Feedback.text.field.name  # type: ignore[attr-defined]
)
FeedbackFilesField: str = (
    models.Feedback.files.field.name
)
FeedbackCreateOnField: str = (
    models.Feedback.created_on.field.name  # type: ignore[attr-defined]
)
FeedbackStatusField: str = (
    models.Feedback.status.field.name  # type: ignore[attr-defined]
)
FeedbackPersonalData: str = (
    models.Feedback.personal_data.field.name
)

FileFeedbackFileField: str = (
    models.FeedbackFile.file.field.name
)
FileFeedbackField: str = (
    models.FeedbackFile.feedback.field.name
)

PersonalDataEmailField: str = (
    models.FeedbackPersonalData.email.field.name  # type: ignore[attr-defined]
)
