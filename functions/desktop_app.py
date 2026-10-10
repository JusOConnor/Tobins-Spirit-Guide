'''The Tobin's Spirit Guide desktop window, built with customtkinter.

Start it by running start_guide.py, or from a notebook cell with:

    from functions.desktop_app import run
    run()

The cell stays busy while the window is open and finishes when you close it.
'''

import customtkinter as ctk

from .data import load_ghosts
from .logic import (
    CONFIRMED,
    ELIMINATED,
    EVIDENCE_CHOICES,
    FOUND,
    ONE_FOUND,
    RULED_OUT,
    TWO_FOUND,
    UNKNOWN,
    format_time,
    get_evidence_types,
    ghost_status,
    new_selections,
    remaining_evidence,
)


TITLE = "Tobin's Spirit Guide"

# Colors for each ghost result, matching the original guide.
STATUS_COLORS = {
    CONFIRMED: '#00c853',
    TWO_FOUND: '#ff9800',
    ONE_FOUND: '#ffd600',
    ELIMINATED: '#262626',
}
OPEN_COLOR = '#e0e0e0'

# Colors for the evidence choice buttons, so you can see each choice at a glance.
CHOICE_COLORS = {
    RULED_OUT: '#c62828',
    UNKNOWN: '#565b5e',
    FOUND: '#2e7d32',
}

# Colors for the evidence names shown beside each ghost.
EVIDENCE_TEXT = '#ffffff'
EVIDENCE_HIGHLIGHT = '#00e676'
EVIDENCE_DIMMED = '#4a4a4a'

# Colors for the timer.
COUNTDOWN_COLOR = '#00e5ff'
OVERTIME_COLOR = '#ff5252'


class SpiritGuideApp(ctk.CTk):
    '''The main window: evidence choices on the left, ghosts on the right.'''

    def __init__(self, ghosts=None):
        ctk.set_appearance_mode('dark')
        super().__init__()

        self.title(TITLE)
        self.ghosts = ghosts if ghosts is not None else load_ghosts()
        self.evidence_types = get_evidence_types(self.ghosts)

        # The evidence buttons and ghost rows, saved so they can be updated later.
        self.evidence_buttons = {}
        self.ghost_rows = {}

        # Everything the timer needs to remember between ticks.
        self.timer_job = None
        self.seconds_left = 0
        self.overtime_seconds = 0

        self.build_layout()
        self.refresh()

        # Closing the window with the X runs the same cleanup as the Quit button.
        self.protocol('WM_DELETE_WINDOW', self.quit_app)

    # Building the window

    def build_layout(self):
        '''Create every part of the window once.'''
        header = ctk.CTkLabel(self, text=TITLE, font=ctk.CTkFont(size=22, weight='bold'))
        header.grid(row=0, column=0, columnspan=2, pady=(12, 6))

        left_side = ctk.CTkFrame(self, fg_color='transparent')
        left_side.grid(row=1, column=0, sticky='nsew', padx=(12, 6), pady=(0, 12))

        right_side = ctk.CTkFrame(self)
        right_side.grid(row=1, column=1, sticky='nsew', padx=(6, 12), pady=(0, 12))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_evidence_section(left_side)
        self.build_controls_section(left_side)
        self.build_details_section(left_side)
        self.build_ghost_section(right_side)

    def build_evidence_section(self, parent):
        '''One row per evidence type, each with a three way choice button.'''
        section = ctk.CTkFrame(parent)
        section.pack(fill='x')

        title = ctk.CTkLabel(section, text='Evidence', font=ctk.CTkFont(size=16, weight='bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(8, 4))

        row = 1
        for evidence in self.evidence_types:
            label = ctk.CTkLabel(section, text=evidence, anchor='w', width=120)
            label.grid(row=row, column=0, sticky='w', padx=(12, 8), pady=3)

            choice_button = ctk.CTkSegmentedButton(
                section,
                values=EVIDENCE_CHOICES,
                command=self.on_choice_changed,
            )
            choice_button.set(UNKNOWN)
            choice_button.grid(row=row, column=1, sticky='ew', padx=(0, 12), pady=3)

            self.evidence_buttons[evidence] = choice_button
            row += 1

        section.grid_columnconfigure(1, weight=1)

    def build_controls_section(self, parent):
        '''The timer display and the row of control buttons.'''
        section = ctk.CTkFrame(parent)
        section.pack(fill='x', pady=12)

        self.timer_label = ctk.CTkLabel(
            section,
            text=format_time(0),
            font=ctk.CTkFont(size=26, weight='bold'),
            text_color=COUNTDOWN_COLOR,
        )
        self.timer_label.grid(row=0, column=0, columnspan=5, pady=(8, 4))

        buttons = [
            ('2 Min', lambda: self.start_timer(2 * 60)),
            ('5 Min', lambda: self.start_timer(5 * 60)),
            ('Stop', self.stop_timer),
            ('Reset', self.reset_evidence),
            ('Quit', self.quit_app),
        ]

        column = 0
        for text, action in buttons:
            button = ctk.CTkButton(section, text=text, width=64, command=action)
            button.grid(row=1, column=column, padx=4, pady=(4, 10))
            section.grid_columnconfigure(column, weight=1)
            column += 1

    def build_details_section(self, parent):
        '''The panel that shows a ghost's strength and weakness when you click its name.'''
        section = ctk.CTkFrame(parent)
        section.pack(fill='both', expand=True)

        self.details_name = ctk.CTkLabel(
            section,
            text='Click a ghost for details',
            font=ctk.CTkFont(size=16, weight='bold'),
        )
        self.details_name.pack(anchor='w', padx=12, pady=(8, 4))

        self.details_strength = ctk.CTkLabel(section, text='', anchor='w', justify='left', wraplength=360)
        self.details_strength.pack(anchor='w', padx=12, pady=2)

        self.details_weakness = ctk.CTkLabel(section, text='', anchor='w', justify='left', wraplength=360)
        self.details_weakness.pack(anchor='w', padx=12, pady=(2, 10))

    def build_ghost_section(self, parent):
        '''One row per ghost: a name button followed by its three evidence types.'''
        row = 0
        for ghost in self.ghosts:
            name = ghost['name']

            name_button = ctk.CTkButton(
                parent,
                text=name,
                width=110,
                text_color='black',
                command=lambda ghost=ghost: self.show_details(ghost),
            )
            name_button.grid(row=row, column=0, padx=(10, 8), pady=3)

            evidence_labels = []
            column = 1
            for evidence in ghost['evidence']:
                label = ctk.CTkLabel(parent, text=evidence, width=110)
                label.grid(row=row, column=column, padx=4, pady=3)
                evidence_labels.append(label)
                column += 1

            self.ghost_rows[name] = {'button': name_button, 'labels': evidence_labels}
            row += 1

        for column in range(1, 4):
            parent.grid_columnconfigure(column, weight=1)

    # Responding to your choices

    def current_selections(self):
        '''Read the choice currently picked on every evidence button.'''
        selections = {}
        for evidence, choice_button in self.evidence_buttons.items():
            selections[evidence] = choice_button.get()
        return selections

    def on_choice_changed(self, choice):
        '''Runs automatically whenever you click any evidence choice.'''
        self.refresh()

    def refresh(self):
        '''Recolor the evidence buttons and every ghost row to match your choices.'''
        selections = self.current_selections()

        for evidence, choice_button in self.evidence_buttons.items():
            color = CHOICE_COLORS[selections[evidence]]
            choice_button.configure(selected_color=color, selected_hover_color=color)

        for ghost in self.ghosts:
            status = ghost_status(ghost, selections)
            row = self.ghost_rows[ghost['name']]

            button_color = STATUS_COLORS.get(status, OPEN_COLOR)
            if status == ELIMINATED:
                name_text_color = EVIDENCE_DIMMED
            else:
                name_text_color = 'black'
            row['button'].configure(
                fg_color=button_color,
                hover_color=button_color,
                text_color=name_text_color,
            )

            # With two pieces found, light up the last piece still to look for.
            still_needed = []
            if status == TWO_FOUND:
                still_needed = remaining_evidence(ghost, selections)

            for evidence, label in zip(ghost['evidence'], row['labels']):
                if status == ELIMINATED:
                    text_color = EVIDENCE_DIMMED
                elif evidence in still_needed:
                    text_color = EVIDENCE_HIGHLIGHT
                else:
                    text_color = EVIDENCE_TEXT
                label.configure(text_color=text_color)

    def reset_evidence(self):
        '''Set every piece of evidence back to Unknown.'''
        starting_choices = new_selections(self.evidence_types)
        for evidence, choice in starting_choices.items():
            self.evidence_buttons[evidence].set(choice)
        self.refresh()

    def show_details(self, ghost):
        '''Fill the details panel with the chosen ghost's strength and weakness.'''
        self.details_name.configure(text=ghost['name'])
        self.details_strength.configure(text=f'Strength: {ghost['strength']}')
        self.details_weakness.configure(text=f'Weakness: {ghost['weakness']}')

    # The timer

    def start_timer(self, seconds):
        '''Count down from the chosen time, then keep counting up in red as overtime.'''
        # Cancel any timer already running so two never tick at once.
        self.cancel_timer_job()
        self.seconds_left = seconds
        self.overtime_seconds = 0
        self.tick()

    def tick(self):
        '''Update the clock once, then schedule the next update one second later.'''
        if self.seconds_left > 0:
            self.timer_label.configure(text=format_time(self.seconds_left), text_color=COUNTDOWN_COLOR)
            self.seconds_left -= 1
        else:
            self.timer_label.configure(text=format_time(self.overtime_seconds), text_color=OVERTIME_COLOR)
            self.overtime_seconds += 1

        self.timer_job = self.after(1000, self.tick)

    def stop_timer(self):
        '''Stop the clock and set it back to zero.'''
        self.cancel_timer_job()
        self.timer_label.configure(text=format_time(0), text_color=COUNTDOWN_COLOR)

    def cancel_timer_job(self):
        '''Cancel the next scheduled clock update, if there is one.'''
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def quit_app(self):
        '''Stop the timer and close the window.'''
        self.cancel_timer_job()
        self.destroy()


def run(ghosts=None):
    '''Open the guide window. Pass your own ghost list to try out changes.'''
    app = SpiritGuideApp(ghosts)
    app.mainloop()
