"""
This is where we implement our UI using tkinter
This file has the MainView class
"""
import os
from pathlib import Path
from tkinter import Tk, Label, ttk, Button, filedialog, LabelFrame, StringVar, Radiobutton, IntVar, Entry, Frame, \
    messagebox
from tkinter.constants import E

from PIL import Image, ImageTk
import fitz

import frontend.constants as c


class MainView:
    def __init__(self) -> None:
        # Components of Main GUI
        self.main_ui_root = Tk()
        self.file_for_ocr = c.IMAGE_PATH_PLACEHOLDER
        self.image = ImageTk.PhotoImage(Image.open("frontend/images/image_placeholder.jpg"))
        self.document_radio_selection = StringVar()
        self.main_ui_warning_label = None
        self.document_radio_seperator = None
        self.start_btn = None
        self.in_radio_btn = None
        self.er_radio_btn = None
        self.fd_radio_btn = None
        self.document_description_label = None
        self.specify_document_label = None
        self.image_preview_seperator = None
        self.document_choose_file_label_seperator = None
        self.document_choose_file_label = None
        self.image_preview_path_label = None
        self.image_preview = None
        self.image_preview_inner_frame = None
        self.image_preview_frame = None
        self.document_choose_file_btn = None
        self.main_ui_heading_seperator = None
        self.main_ui_primary_heading = None
        self.main_ui_root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_view(self) -> None:
        # Basic definitions of gui window
        self.main_ui_root.title(c.OCR_TITLE)
        self.main_ui_root.geometry(c.MAIN_WINDOW_SIZE)
        self.main_ui_root.iconbitmap("./frontend/images/main_ui_logo.ico")

        # Main Heading
        self.main_ui_primary_heading = Label(self.main_ui_root, text=c.MAIN_UI_PRIMARY_HEADING, padx=10, pady=5,
                                             anchor=E, font=c.FONT_LARGE)
        self.main_ui_primary_heading.grid(row=0, column=0, sticky="w")

        self.main_ui_heading_seperator = ttk.Separator(self.main_ui_root, orient="horizontal")
        self.main_ui_heading_seperator.grid(row=1, column=0, sticky="ew", columnspan=3)

        # Choose File
        self.document_choose_file_label = Label(self.main_ui_root, text=c.DOCUMENT_CHOOSE_LABEL_TEXT, padx=10, pady=5, font=c.FONT_MEDIUM)
        self.document_choose_file_label.grid(row=2, column=0, sticky="w")

        self.document_choose_file_label_seperator = ttk.Separator(self.main_ui_root, orient="horizontal")
        self.document_choose_file_label_seperator.grid(row=4, column=0, sticky="ew", columnspan=3)

        self.document_choose_file_btn = Button(self.main_ui_root, text=c.CHOOSE_BTN_TEXT,
                                               command=self.open_file_for_ocr, borderwidth=5,
                                               activebackground=c.BTN_ACTIVE_BG_COLOR, font=c.FONT_SMALL)
        self.document_choose_file_btn.grid(row=2, column=1, padx=5, pady=5)

        # Image Preview
        self.image_preview_frame = LabelFrame(self.main_ui_root, bg=c.IMAGE_FRAME_COLOR, padx=10, pady=10,
                                              borderwidth=5)
        self.image_preview_frame.grid(row=5, column=0, columnspan=3)
        self.image_preview_inner_frame = LabelFrame(self.image_preview_frame, bg=c.IMAGE_FRAME_COLOR, borderwidth=1)
        self.image_preview_inner_frame.grid(row=2, column=0, columnspan=3)
        self.image_preview_path_label = Label(self.image_preview_frame, text=self.file_for_ocr, borderwidth=2,
                                              relief="solid", anchor="w", font=c.FONT_SMALL)
        self.image_preview_path_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.image_preview = Label(self.image_preview_inner_frame, image=self.image)
        self.image_preview.grid(row=0, column=0)

        self.image_preview_seperator = ttk.Separator(self.main_ui_root, orient="horizontal")
        self.image_preview_seperator.grid(row=6, column=0, sticky="ew", columnspan=3)

        # Radio Selection
        self.specify_document_label = Label(self.main_ui_root, text=c.SPECIFY_LABEL_TEXT, font=c.FONT_MEDIUM)
        self.specify_document_label.grid(row=7, column=0, sticky="w")

        self.document_description_label = Label(self.main_ui_root, text=c.DOCUMENT_RADIO_DESCRIPTION_TEXT, font=c.FONT_SMALL,
                                                fg="#6c757d")
        self.document_description_label.grid(row=8, column=0)

        self.fd_radio_btn = Radiobutton(self.main_ui_root, text=c.FD_RADIO_BTN_TEXT,
                                        variable=self.document_radio_selection, value="fd", font=c.FONT_SMALL)
        self.fd_radio_btn.grid(row=9, column=0, sticky="w")
        self.er_radio_btn = Radiobutton(self.main_ui_root, text=c.ER_RADIO_BTN_TEXT,
                                        variable=self.document_radio_selection, value="er", font=c.FONT_SMALL)
        self.er_radio_btn.grid(row=9, column=1)
        self.in_radio_btn = Radiobutton(self.main_ui_root, text=c.IN_RADIO_BTN_TEXT,
                                        variable=self.document_radio_selection, value="in", font=c.FONT_SMALL)
        self.in_radio_btn.grid(row=9, column=2)
        self.fd_radio_btn.select()

        self.document_radio_seperator = ttk.Separator(self.main_ui_root, orient="horizontal")
        self.document_radio_seperator.grid(row=10, column=0, sticky="ew", columnspan=3)

        # Start Button
        self.start_btn = Button(self.main_ui_root, text=c.START_BTN_TEXT, borderwidth=5,
                                activebackground="#adb5bd", command=self.start_conversion, font=c.FONT_SMALL)
        self.start_btn.grid(row=11, column=2, columnspan=1, sticky="e", padx=10, pady=10)

        self.main_ui_warning_label = Label(self.main_ui_root, text="", fg=c.WARNING_TEXT_COLOR)
        self.main_ui_warning_label.grid(row=12, column=0, columnspan=3)

    def run_main_view(self) -> None:
        self.main_ui_root.mainloop()

    def open_file_for_ocr(self) -> None:
        # Resets Warning label if it is displayed
        self.main_ui_warning_label.config(text="")

        # File open and preview operation
        self.file_for_ocr = filedialog.askopenfilename(title=c.CHOOSE_FILE_DIALOG_TEXT)
        if self.file_for_ocr.lower().endswith(".pdf"):
            pdf_document = fitz.open(self.file_for_ocr)
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            self.image = ImageTk.PhotoImage(img.resize(c.IMAGE_SIZE))
        else:
            img = Image.open(self.file_for_ocr)
            self.image = ImageTk.PhotoImage(img.resize(c.IMAGE_SIZE))
        self.image_preview_path_label.config(text=self.file_for_ocr)
        self.image_preview.config(image=self.image)

    def get_document_radio_selection(self) -> str:
        return self.document_radio_selection.get()

    def get_file_for_ocr(self) -> str:
        return self.file_for_ocr

    def start_conversion(self) -> None:
        # Check to determine if a file is chosen
        if self.file_for_ocr == c.IMAGE_PATH_PLACEHOLDER:
            self.main_ui_warning_label.config(text=c.MAIN_UI_WARNING_TEXT)
        else:
            self.main_ui_root.destroy()  # Close the GUI

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.main_ui_root.destroy()


class ExcelView:
    def __init__(self) -> None:
        self.excel_ui_root = Tk()
        self.save_option_selection = IntVar()
        self.sheet_selection = IntVar()
        self.append_option_frame = None
        self.save_new_option_frame = None
        self.excel_primary_heading = None
        self.excel_primary_heading_seperator = None
        self.success_msg_label = None
        self.save_option_label = None
        self.save_new_radio_btn = None
        self.append_radio_btn = None
        self.save_filename = None
        self.saving_format_label = None
        self.single_sheet_radio_btn = None
        self.multi_sheet_radio_btn = None
        self.save_filename_label = None
        self.save_filename_field = None
        self.browse_folder_btn = None
        self.select_save_location_label = None
        self.new_save_location_path_label = None
        self.excel_file = None
        self.save_location_path_label = None
        self.file_to_append_path_label = None
        self.choose_file_to_append_btn = None
        self.select_file_to_append_label = None
        self.save_option_seperator = None
        documents_path = Path.home() / "Documents"
        self.folder_path = str(documents_path)
        self.new_folder_path = None
        self.save_btn = None
        self.excel_ui_warning_label = None
        self.excel_ui_root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_excel_view(self) -> None:
        self.excel_ui_root.title(c.OCR_TITLE)
        self.excel_ui_root.geometry(c.EXCEL_WINDOW_SIZE)
        self.excel_ui_root.iconbitmap("./frontend/images/excel_ui_logo.ico")

        self.excel_primary_heading = Label(self.excel_ui_root, text=c.EXCEL_UI_PRIMARY_HEADING, anchor=E, font=c.FONT_LARGE)
        self.excel_primary_heading.grid(row=0, column=0, sticky="w", pady=5, padx=10)

        self.excel_primary_heading_seperator = ttk.Separator(self.excel_ui_root, orient="horizontal")
        self.excel_primary_heading_seperator.grid(row=1, column=0, sticky="ew", columnspan=2, pady=5)

        self.success_msg_label = Label(self.excel_ui_root, text=c.EXCEL_SUCCESS_MSG_TEXT, anchor=E, font=c.FONT_SMALL, fg="green")
        self.success_msg_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.save_option_label = Label(self.excel_ui_root, text=c.SAVE_OPTION_TEXT, anchor=E, font=c.FONT_MEDIUM)
        self.save_option_label.grid(row=3, column=0, sticky="w", padx=10)

        self.save_new_radio_btn = Radiobutton(self.excel_ui_root, text=c.SAVE_NEW_RADIO_BTN_TEXT,
                                              variable=self.save_option_selection, value=1,
                                              command=self.save_option_command, font=c.FONT_SMALL)
        self.save_new_radio_btn.grid(row=4, column=0, sticky="w", padx=15)
        self.append_radio_btn = Radiobutton(self.excel_ui_root, text=c.APPEND_RADIO_BTN_TEXT,
                                            variable=self.save_option_selection, value=2,
                                            command=self.save_option_command, font=c.FONT_SMALL)
        self.append_radio_btn.grid(row=5, column=0, sticky="w", padx=15)

        self.save_option_seperator = ttk.Separator(self.excel_ui_root, orient="horizontal")
        self.save_option_seperator.grid(row=6, column=0, sticky="ew", columnspan=2, pady=5)

        self.excel_ui_warning_label = Label(self.excel_ui_warning_label, text="", fg=c.WARNING_TEXT_COLOR)
        self.excel_ui_warning_label.grid(row=8, column=0, columnspan=3)

        # Different GUI depending on Save option

        # Save in new file option
        self.save_new_option_frame = Frame(self.excel_ui_root)
        self.saving_format_label = Label(self.save_new_option_frame, text=c.SAVING_FORMAT_TEXT, anchor=E, font=c.FONT_MEDIUM)
        self.saving_format_label.grid(row=0, column=0, sticky="w")

        self.single_sheet_radio_btn = Radiobutton(self.save_new_option_frame, text=c.SINGLE_SHEET_RADIO_BTN_TEXT,
                                                  variable=self.sheet_selection, value=1, font=c.FONT_SMALL)
        self.single_sheet_radio_btn.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.multi_sheet_radio_btn = Radiobutton(self.save_new_option_frame, text=c.MULTI_SHEET_RADIO_BTN_TEXT,
                                                 variable=self.sheet_selection, value=2, font=c.FONT_SMALL)
        self.multi_sheet_radio_btn.grid(row=1, column=1, sticky="w", padx=5, pady=10)

        self.save_filename_label = Label(self.save_new_option_frame, text=c.SAVE_FILENAME_TEXT, anchor=E, font=c.FONT_MEDIUM)
        self.save_filename_label.grid(row=2, column=0, sticky="w")

        self.save_filename_field = Entry(self.save_new_option_frame, width=50, borderwidth=5, font=c.FONT_MEDIUM, bg="#dee2e6")
        self.save_filename_field.grid(row=3, column=0, sticky="w", padx=5, columnspan=2)

        self.select_save_location_label = Label(self.save_new_option_frame, text=c.SELECT_SAVE_LOCATION_TEXT, anchor=E, font=c.FONT_MEDIUM)
        self.select_save_location_label.grid(row=4, column=0, sticky="w")

        self.browse_folder_btn = Button(self.save_new_option_frame, text=c.BROWSE_FOLDER_BTN_TEXT, borderwidth=5,
                                        activebackground="#adb5bd", command=self.browse_folder, font=c.FONT_SMALL)
        self.browse_folder_btn.grid(row=4, column=1, padx=5, pady=5)
        self.save_location_path_label = Label(self.save_new_option_frame, text=self.folder_path, borderwidth=2,
                                              relief="solid", anchor="w", font=c.FONT_MEDIUM)
        self.save_location_path_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.save_btn = Button(self.save_new_option_frame, text=c.SAVE_BTN_TEXT, borderwidth=5,
                               activebackground=c.BTN_ACTIVE_BG_COLOR, padx=10, command=self.save_btn_command, font=c.FONT_SMALL)
        self.save_btn.grid(row=6, column=1, padx=5, pady=5, sticky="e")

        # Append to existing file option
        self.append_option_frame = Frame(self.excel_ui_root)

        self.select_file_to_append_label = Label(self.append_option_frame, text=c.SELECT_FILE_TO_APPEND_BTN_TEXT,
                                                 anchor=E, font=c.FONT_MEDIUM)
        self.select_file_to_append_label.grid(row=0, column=0, sticky="w")

        self.choose_file_to_append_btn = Button(self.append_option_frame, text=c.CHOOSE_BTN_TEXT, borderwidth=5,
                                                activebackground="#adb5bd", command=self.open_excel_file, font=c.FONT_SMALL)
        self.choose_file_to_append_btn.grid(row=0, column=1, padx=25, pady=5)
        self.file_to_append_path_label = Label(self.append_option_frame, borderwidth=2, relief="solid", anchor="w", font=c.FONT_MEDIUM)
        self.file_to_append_path_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.select_save_location_label = Label(self.append_option_frame, text=c.SELECT_SAVE_LOCATION_OPTIONAL_TEXT,
                                                anchor=E, font=c.FONT_MEDIUM)
        self.select_save_location_label.grid(row=2, column=0, sticky="w")
        self.browse_folder_btn = Button(self.append_option_frame, text=c.BROWSE_FOLDER_BTN_TEXT, borderwidth=5,
                                        activebackground="#adb5bd", command=self.browse_folder, font=c.FONT_SMALL)
        self.browse_folder_btn.grid(row=2, column=1, padx=30, pady=5)
        self.new_save_location_path_label = Label(self.append_option_frame, text=self.new_folder_path, borderwidth=2,
                                                  relief="solid", anchor="w", font=c.FONT_MEDIUM)
        self.new_save_location_path_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.save_btn = Button(self.append_option_frame, text=c.SAVE_BTN_TEXT, borderwidth=5,
                               activebackground=c.BTN_ACTIVE_BG_COLOR, padx=10, command=self.save_btn_command, font=c.FONT_SMALL)
        self.save_btn.grid(row=4, column=1, padx=5, pady=5, sticky="e")

    def run_excel_view(self) -> None:
        self.excel_ui_root.mainloop()

    def save_option_command(self) -> None:
        if self.get_save_option_selection() == 1:
            self.save_new_option_frame.grid(row=7, column=0, padx=10, pady=10)
            self.append_option_frame.grid_forget()
        elif self.get_save_option_selection() == 2:
            self.append_option_frame.grid(row=7, column=0, padx=10, pady=10)
            self.save_new_option_frame.grid_forget()

    def browse_folder(self) -> None:
        self.folder_path = self.new_folder_path = filedialog.askdirectory()
        if self.get_save_option_selection() == 1:
            self.save_location_path_label.config(text=self.folder_path)
        elif self.get_save_option_selection() == 2:
            self.new_save_location_path_label.config(text=self.new_folder_path)

    def open_excel_file(self) -> None:
        self.excel_file = filedialog.askopenfilename(title=c.CHOOSE_FILE_DIALOG_TEXT,
                                                     filetypes=(("Excel files", "*.xlsx;*.xls"),))
        self.file_to_append_path_label.config(text=self.excel_file)

    def get_save_option_selection(self) -> int:
        return self.save_option_selection.get()

    def get_excel_file(self) -> str:
        return self.excel_file

    def get_sheet_selection(self) -> int:
        return self.sheet_selection.get()

    def get_save_filename(self) -> str:
        return self.save_filename.strip()

    def get_folder(self) -> str:
        return self.folder_path

    def get_new_folder(self) -> str:
        return self.new_folder_path

    def get_save_location(self) -> str:
        return f'{self.get_folder()}/{self.get_save_filename()}.xlsx'

    def get_new_save_location(self) -> str | None:
        if self.get_new_folder() is None:
            return None
        else:
            file_name = os.path.basename(self.get_excel_file())
            return f'{self.get_new_folder()}/{file_name}'

    def store_save_filename(self) -> None:
        self.save_filename = self.save_filename_field.get()

    def save_btn_command(self) -> None:
        self.store_save_filename()
        self.excel_ui_warning_label.config(text="")

        if self.get_save_option_selection() == 1:
            if self.get_sheet_selection() == 1 or self.get_sheet_selection() == 2:
                if self.get_save_filename().strip():
                    self.excel_ui_root.destroy()
                else:
                    self.excel_ui_warning_label.config(text=c.EXCEL_UI_SAVE_FILENAME_WARNING_TEXT)
            else:
                self.excel_ui_warning_label.config(text=c.EXCEL_UI_SAVE_FORMAT_WARNING_TEXT)
        elif self.get_save_option_selection() == 2:
            if self.get_excel_file() is None:
                self.excel_ui_warning_label.config(text=c.EXCEL_UI_APPEND_FILE_WARNING_TEXT)
            else:
                self.excel_ui_root.destroy()
        else:
            self.excel_ui_warning_label.config(text=c.EXCEL_UI_SAVE_OPTION_WARNING_TEXT)

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.excel_ui_root.destroy()


class ExitView:
    def __init__(self) -> None:
        self.exit_ui_root = Tk()
        self.exit_primary_heading = None
        self.scan_more_btn = None
        self.exit_btn = None
        self.exit_ui_root.protocol("WM_DELETE_WINDOW", self.exit_command)

    def create_exit_view(self, app_function) -> None:
        self.exit_ui_root.title(c.OCR_TITLE)
        self.exit_ui_root.geometry(c.EXIT_WINDOW_SIZE)
        self.exit_ui_root.iconbitmap("./frontend/images/exit_ui_logo.ico")

        self.exit_primary_heading = Label(self.exit_ui_root, text=c.EXIT_UI_PRIMARY_HEADING,
                                          anchor=E, font=c.FONT_MEDIUM)
        self.exit_primary_heading.grid(row=0, column=0, sticky="w", pady=5, padx=10)

        self.scan_more_btn = Button(self.exit_ui_root, text=c.SCAN_MORE_BTN_TEXT, borderwidth=5,
                                    activebackground="#adb5bd", padx=10,
                                    command=lambda: self.scan_more_command(app_function), font=c.FONT_SMALL)
        self.scan_more_btn.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.exit_btn = Button(self.exit_ui_root, text=c.EXIT_BTN_TEXT, borderwidth=5,
                               activebackground="#ffe6e6", padx=10, command=self.exit_command, font=c.FONT_SMALL)
        self.exit_btn.grid(row=1, column=1, padx=5, pady=5, sticky="e")

    def run_exit_view(self) -> None:
        self.exit_ui_root.mainloop()

    def scan_more_command(self, app_function) -> None:
        self.exit_ui_root.destroy()
        app_function()

    def exit_command(self) -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.exit_ui_root.destroy()
