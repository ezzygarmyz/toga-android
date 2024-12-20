from android import R
from android.app import AlertDialog
from android.content import Context, DialogInterface, ClipboardManager, ClipData
from android.widget import EditText, Toast
from android.text import InputType
from java import dynamic_proxy, cast

import toga


class OnClickListener(dynamic_proxy(DialogInterface.OnClickListener)):
    def __init__(self, fn=None, value=None):
        super().__init__()
        self._fn = fn
        self._value = value

    def onClick(self, _dialog, _which):
        self._fn(self._value)


class BaseDialog:
    def show(self, host_window, future):
        self.future = future

        if self.native:
            # Show the dialog. Don't differentiate between app and window modal dialogs.
            self.native.show()
        else:
            # Dialog doesn't have an implementation. This can't be covered, as
            # the testbed shortcuts the test before showing the dialog.
            self.future.set_result(None)  # pragma: no cover


class TextDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        positive_text,
        negative_text=None,
        icon=None,
    ):
        super().__init__()

        self.native = AlertDialog.Builder(toga.App.app.current_window._impl.app.native)
        self.native.setCancelable(False)
        self.native.setTitle(title)
        self.native.setMessage(message)
        if icon is not None:
            self.native.setIcon(icon)

        self.native.setPositiveButton(
            positive_text,
            OnClickListener(
                self.completion_handler,
                True if (negative_text is not None) else None,
            ),
        )
        if negative_text is not None:
            self.native.setNegativeButton(
                negative_text, OnClickListener(self.completion_handler, False)
            )

    def completion_handler(self, return_value: bool) -> None:
        self.future.set_result(return_value)


class InputDialog(TextDialog):
    def __init__(
        self,
        title,
        message,
        positive_text="OK",
        negative_text="Cancel",
        initial_text=""
    ):
        super().__init__(
            title=title,
            message=message,
            positive_text=positive_text,
            negative_text=negative_text,
        )
        
        
        self.input_field = EditText(toga.App.app.current_window._impl.app.native)
        self.input_field.setText(initial_text)
        self.input_field.setInputType(InputType.TYPE_CLASS_TEXT)
        
        self.native.setView(self.input_field)

    def completion_handler(self, return_value: bool) -> None:
        if return_value:
            input_text = self.input_field.getText().toString()
            self.future.set_result(input_text)
        else:
            self.future.set_result(None)

        context = toga.App.app.current_window._impl.app.native
        input_method_manager = context.getSystemService(Context.INPUT_METHOD_SERVICE)
        if input_method_manager:
            input_method_manager.hideSoftInputFromWindow(
                self.input_field.getWindowToken(), 0
            )


class PasswordDialog(InputDialog):
    def __init__(
        self,
        title,
        message,
        positive_text="OK",
        negative_text="Cancel",
        initial_text="",
    ):
        super().__init__(
            title=title,
            message=message,
            positive_text=positive_text,
            negative_text=negative_text,
            initial_text=initial_text,
        )

        self.input_field.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD)

    def completion_handler(self, return_value: bool) -> None:
        if return_value:
            password = self.input_field.getText().toString()
            self.future.set_result(password)  
        else:
            self.future.set_result(None)

        context = toga.App.app.current_window._impl.app.native
        input_method_manager = context.getSystemService(Context.INPUT_METHOD_SERVICE)
        if input_method_manager:
            input_method_manager.hideSoftInputFromWindow(
                self.input_field.getWindowToken(), 0
            )


class InfoDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
        )


class QuestionDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="Yes",
            negative_text="No",
        )


class ConfirmDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
            negative_text="Cancel",
        )


class ErrorDialog(TextDialog):
    def __init__(self, title, message):
        super().__init__(
            title=title,
            message=message,
            positive_text="OK",
            icon=R.drawable.ic_dialog_alert,
        )


class StackTraceDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        **kwargs,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.StackTraceDialog()")
        self.native = None


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        filename,
        initial_directory,
        file_types=None,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.SaveFileDialog()")
        self.native = None


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        file_types,
        multiple_select,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.OpenFileDialog()")
        self.native = None


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        title,
        initial_directory,
        multiple_select,
    ):
        super().__init__()

        toga.App.app.factory.not_implemented("dialogs.SelectFolderDialog()")
        self.native = None


class CopyText():
    def __init__(
        self,
        text,
        message,
    ):
        super().__init__()

        self.clipboard_manager = None
        context = toga.App.app.current_window._impl.app.native
        clipboard_service = context.getSystemService(
            context.CLIPBOARD_SERVICE
        )
        self.clipboard_manager = cast(
            ClipboardManager,
            clipboard_service
        )
        clip_data = ClipData.newPlainText("button", text)
        self.clipboard_manager.setPrimaryClip(clip_data)
        toast = Toast.makeText(context, message, Toast.LENGTH_SHORT)
        toast.show()



class PasteText():
    def __init__(
        self
    ):
        super().__init__()

        self.clipboard_manager = None
        context = toga.App.app.current_window._impl.app.native
        clipboard_service = context.getSystemService(
            context.CLIPBOARD_SERVICE
        )
        self.clipboard_manager = cast(
            ClipboardManager,
            clipboard_service
        )
        if self.clipboard_manager.hasPrimaryClip():
            clip_data = self.clipboard_manager.getPrimaryClip()
            clip_data.getItemAt(0).getText()