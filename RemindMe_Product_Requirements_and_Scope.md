# RemindMe --- Product Requirements & Scope Document

**Document type:** Product Requirements Document (PRD)\
**Product:** RemindMe\
**Platform:** Windows desktop\
**Distribution:** Open-source project; Windows installer (PyInstaller
one-directory build packaged with Inno Setup) through GitHub Releases\
**Status:** Product scope updated; detailed low-level design pending\
**Version:** 0.2 (adds global hotkey, application-owned alerts, Inno
Setup installer and code-signing plan; positioning section rewritten)\
**Last updated:** 10 November 2026

------------------------------------------------------------------------

## 1. Product overview

RemindMe is a lightweight, offline-first Windows desktop reminder
application designed to make creating, managing, and recovering
reminders exceptionally quick and reliable.

The application is intended for people who manage many independent
responsibilities and frequently need to capture tasks without navigating
a calendar or a complex productivity application.

The primary interaction should be simple:

1.  Press the global hotkey, or click the desktop shortcut or the system
    tray icon.
2.  A small **New Reminder** window appears.
3.  Enter what needs to be remembered and when it should happen.
4.  Create the reminder.
5.  RemindMe runs quietly in the background and notifies the user when
    it is due.

Users can open a separate **View Reminders** window to inspect, edit,
delete, complete, or reschedule their reminders.

When a reminder falls due, RemindMe shows its own alert window with two
actions: **Done** and **Reschedule**. A Windows notification may
accompany the alert, but the alert window is the primary delivery
mechanism, because a toast alone can be suppressed by Focus Assist or
dismissed unseen.

A key product requirement is missed-reminder recovery. If a reminder
becomes due while the laptop is shut down, sleeping, or the application
is unavailable, it must remain pending and be surfaced when the
application next runs and can reconcile its stored reminders.

RemindMe is not intended to become a full calendar, project-management
platform, or AI productivity assistant. Its value comes from
low-friction capture, dependable local scheduling, clear task context,
and sensible recovery behaviour.

## 2. Product philosophy and goals

### 2.1 Product philosophy

> Capture a task in seconds, schedule it naturally, and never silently
> lose it just because the laptop was unavailable.

The product should follow these principles:

-   **Frictionless capture:** Creating a reminder should require as few
    interactions as reasonably possible.
-   **Task-first, not calendar-first:** The central object is a task or
    responsibility with a due time, not a calendar event.
-   **Two complementary input methods:** Users can enter structured
    title/date/time fields or describe a reminder in natural language.
-   **Local-first and offline-first:** Reminder creation, storage,
    scheduling, and recovery must work without an internet connection.
-   **Persistent by default:** A reminder remains pending until the user
    explicitly completes or deletes it, or reschedules it.
-   **Recoverable:** Missed reminders must be detected and surfaced
    after startup or system resume.
-   **Lightweight:** The background process should consume minimal
    memory and CPU.
-   **Focused scope:** Avoid features that do not materially improve
    reminder capture, delivery, management, or reliability.
-   **Transparent and privacy-conscious:** The application should not
    transmit reminder content or collect telemetry.

### 2.2 Primary goals

1.  Make reminder creation available instantly through a global hotkey,
    and in a few clicks from the Windows desktop or system tray.
2.  Support both conventional date/time entry and natural-language
    scheduling.
3.  Deliver due reminders through an application-owned alert window
    (with Done and Reschedule), supported by a Windows notification.
4.  Persist reminders locally so they survive application closure and
    system restarts.
5.  Detect reminders missed during shutdown, sleep, or application
    unavailability.
6.  Give users explicit **Done** and **Reschedule** actions for overdue
    reminders.
7.  Provide a simple interface for viewing and managing all reminders.
8.  Distribute the application as a per-user Windows installer
    (PyInstaller one-directory build + Inno Setup) through GitHub
    Releases.
9.  Keep the application resource-efficient and minimize its security
    attack surface.

### 2.3 Non-goals

The initial product is not intended to provide:

-   A complete calendar or event-planning system.
-   Project-management boards, task dependencies, or team collaboration.
-   Cloud synchronization or multi-device synchronization.
-   User accounts or authentication.
-   A hosted backend or remote database.
-   AI-based task planning or automatic prioritization.
-   An LLM/API dependency for natural-language parsing.
-   A mobile application.
-   A full-featured alarm-clock replacement.
-   Productivity analytics, streaks, or gamification.

## 3. Intended users and use cases

The initial user is someone who manages multiple parallel
responsibilities and needs a reliable way to capture individual tasks
without interrupting their current work.

Example responsibilities include:

-   Internship deliverables and follow-ups.
-   Research tasks and literature surveys.
-   College assignments and examination preparation.
-   Personal projects.
-   Open-source contributions and application deadlines.
-   Everyday personal tasks.

Representative use cases:

1.  A user remembers a task while working and wants to schedule it for
    two hours later.
2.  A user wants to create a reminder for a specific date and time.
3.  A user wants to type a sentence such as "Remind me to review the
    steganography paper tomorrow at 10 AM."
4.  A user wants to inspect all upcoming and overdue reminders.
5.  A user wants to edit or delete a reminder.
6.  A user completes a task and marks it Done.
7.  A user cannot complete a task at the scheduled time and chooses a
    new time through Reschedule.
8.  A laptop is shut down when a reminder becomes due; the reminder is
    recovered after the next startup.
9.  A laptop sleeps through a reminder; the reminder is recovered after
    resume.
10. The application is closed or restarted; stored reminders remain
    available and are reconciled on the next launch.

## 4. Product positioning

RemindMe is a lightweight, task-oriented reminder manager for Windows. It
covers one narrow lifecycle: capture an individual responsibility, give
it a time, be notified when it is due, and keep it actionable until it
is completed or rescheduled.

### 4.1 Scope of the product

RemindMe is:

- A quick-capture utility for individual, time-specific tasks.
- A small reminder manager with upcoming, overdue, and completed views.
- A local Windows application that needs no account and no internet
  connection at runtime.

RemindMe is not:

- A project-management or team collaboration tool.
- A notes workspace or knowledge base.
- A calendar for meetings and appointments.
- A wake-up alarm clock.

Because reminders can be viewed, edited, completed, deleted, and
rescheduled, the application has a small amount of task-management
behaviour. It should not grow into project hierarchies, dependencies,
boards, team assignment, or analytics within the initial scope.

### 4.2 How it relates to existing tools

Many existing tools already overlap with parts of RemindMe, and some
already offer quick-add and natural-language dates. RemindMe does not
assume otherwise. The table below describes where each kind of tool fits
best and what RemindMe does differently.

| Kind of tool | Best suited for | What RemindMe does differently |
|---|---|---|
| Calendar applications (for example Google Calendar, Outlook) | Meetings, appointments, time-blocking, seeing commitments across a week. Most also support simple tasks. | Opens straight into a small capture window instead of a calendar grid; concentrates on single reminders rather than a schedule of events. |
| Task managers (for example Todoist, Microsoft To Do, Trello, Notion) | Organizing work across projects, lists, labels, priorities, and teams. | No projects, labels, or sync; single-user and local. Intended to sit beside a larger task manager for quick time-specific reminders, not replace it. |
| Alarm applications | Signalling that a particular time has arrived. | Carries the task description and a lifecycle: the reminder stays pending, with Done and Reschedule actions, until the user resolves it. |

Three design choices define RemindMe:

- **Fast capture:** a global hotkey, tray icon, or shortcut opens a small
  New Reminder window, with natural-language entry available.
- **Local and private:** no account, backend, telemetry, or runtime
  network access.
- **Reminders are not lost:** a reminder stays pending after its time
  passes, is delivered through an alert the user must act on, and is
  recovered after shutdown, sleep, or the application being closed.

A user who already has a broader task system may still choose RemindMe
for these quick, time-specific reminders.

### 4.3 Platform boundary

A Windows desktop application cannot notify the user while the computer
is powered off. RemindMe recovers reminders when Windows starts or
resumes and the application can run. It does not replace a dedicated
alarm clock, and a full alarm-clock mode is out of scope for the initial
release. A repeating or sound-based alert mode for selected reminders may
be considered later.

### 4.4 Product promise

**Capture it quickly. Get reminded. If you miss it, it will still be
there when you return.**

## 5. Platform and application lifecycle

### 5.1 Target platform

-   Windows desktop only for the initial release.
-   Distribution as a standalone Windows executable.
-   No internet connection required at runtime.
-   No cloud account or server dependency.

### 5.2 Startup and background operation

-   RemindMe should be configured to start automatically after the
    current Windows user logs in.
-   On startup, the application should initialize its background
    services, open its local database, reconcile overdue reminders, and
    schedule the next upcoming reminder.
-   The application should remain running in the background when its
    windows are closed.
-   The user should be able to terminate the application explicitly
    through a system tray menu.
-   The application should prevent accidental duplicate instances.
-   The application should not require administrator privileges.
-   The application should register a global hotkey (see 5.3) while it is
    running and release it on exit.

### 5.3 Opening the application

Any of the following should open the **New Reminder** interface:

-   Pressing the global hotkey from any application.
-   Clicking the desktop or Start Menu shortcut.
-   Clicking the RemindMe system tray icon.

The global hotkey is the primary fast-capture path. Requirements:

-   It is registered with the Windows hotkey API (`RegisterHotKey`), not
    a global keyboard hook, so the application never observes
    keystrokes other than its own hotkey.
-   If the hotkey is already in use by another application, RemindMe
    still starts, tells the user the hotkey is unavailable, and keeps
    the tray icon and shortcut paths working.
-   The hotkey can be changed through a simple setting; a full
    customization interface may come later.
-   Pressing the hotkey while New Reminder is already open brings it to
    the front rather than opening another window.
-   The default combination is decided in low-level design. Combinations
    using Ctrl+Alt act as AltGr on some keyboard layouts and must be
    evaluated before being chosen.

If RemindMe is already running in the background, the shortcut should
activate the existing process rather than start a second instance.

### 5.4 Closing and exiting

-   Closing the New Reminder window should hide or close that window
    without terminating the background application.
-   Closing the View Reminders window should not terminate the
    application.
-   A clearly accessible Exit command in the tray menu should terminate
    the application.
-   The exact window-close and tray-menu interaction should be
    consistent and documented.

## 6. User workflows

### 6.1 First launch

1.  The user installs RemindMe using the Windows installer.
2.  The application initializes its local data directory and database.
3.  The application offers or configures startup registration for the
    current Windows user.
4.  The application starts in the background.
5.  The user can open New Reminder with the hotkey, the desktop
    shortcut, or the tray icon.

Startup registration is offered as an installer option and can be
changed later; it must be transparent and user-controlled.

### 6.2 Create a reminder using structured fields

1.  User presses the hotkey, or clicks the desktop shortcut or tray icon.
2.  The New Reminder window appears.
3.  User enters a reminder title.
4.  User selects a date.
5.  User selects a time.
6.  User optionally uses a quick-time preset.
7.  User selects Create Reminder.
8.  The application validates the input and stores the reminder.
9.  The application updates its next scheduled notification.
10. The interface provides confirmation and returns to its default state
    or closes according to the final interaction design.

### 6.3 Create a reminder using natural language

1.  User opens New Reminder.
2.  User enters a sentence in the natural-language input area.
3.  The local parser extracts a task description and date/time
    expression.
4.  The application displays the interpreted title, date, and time.
5.  User reviews and can correct the parsed values.
6.  User confirms creation.
7.  The reminder is stored through the same reminder-management path
    used by structured entry.

Natural-language parsing must be local and deterministic for the MVP. It
must not require an LLM, external API, or network request.

If the input is ambiguous, incomplete, or cannot be interpreted
confidently, the application should ask the user to correct or complete
the structured fields rather than silently guessing.

### 6.4 Receive a reminder while Windows is running

1.  The reminder reaches its scheduled time.
2.  RemindMe shows its own **alert window** with the reminder title, the
    scheduled time, and two actions: **Done** and **Reschedule**.
3.  RemindMe may also raise a Windows notification to draw attention.
    The notification is supplementary: it can be suppressed by Focus
    Assist or Do Not Disturb, or dismissed into the Action Center, so
    the alert window does not depend on it.
4.  The alert stays visible until the user acts on it.
5.  If the user closes the alert without choosing an action, the
    reminder remains pending, is shown as overdue, and stays reachable
    from the tray and View Reminders.
6.  If several reminders are due together, they appear in one
    consolidated alert rather than separate windows.

Whether the alert takes keyboard focus is a low-level design decision;
it must not steal focus in a way that sends the user's in-progress
typing to the alert.

### 6.5 Recover a reminder missed during shutdown or sleep

Example: a reminder is scheduled for 8:00 PM, but the laptop is
unavailable until 11:00 PM.

1.  Windows starts or resumes.
2.  RemindMe runs or receives the relevant resume event.
3.  The application queries locally stored pending reminders.
4.  It compares their scheduled timestamps with the current time.
5.  It identifies overdue reminders.
6.  It presents a recovery interface showing the reminder title,
    original scheduled time, and how overdue it is.
7.  The user chooses Done or Reschedule.

The application must not mark reminders completed merely because their
scheduled time has passed.

If multiple reminders are overdue, they should be presented in a
consolidated recovery interface rather than creating an uncontrolled
burst of separate notifications.

### 6.6 Complete a reminder

1.  User selects Done.
2.  The reminder status changes to Completed.
3.  The completion timestamp is stored.
4.  The reminder no longer appears in the pending/upcoming list.
5.  It remains accessible in the completed section.

### 6.7 Reschedule a reminder

1.  User selects Reschedule (from the alert, the recovery window, or
    View Reminders).
2.  RemindMe offers:
    -   **Snooze** presets for one-click delays. Proposed: 10 minutes,
        1 hour, 3 hours, tomorrow morning. The final list is decided in
        low-level design.
    -   **Pick date and time** for a specific new time.
3.  The application validates and saves the new schedule.
4.  The reminder returns to the pending state.
5.  The scheduler is updated.

**Terminology:** *Reschedule* is the action. *Snooze* is the label for
the quick-delay presets inside it, and delays are counted from the
current time. Snooze is not a separate top-level action, so every alert
has exactly two choices: Done or Reschedule.

### 6.8 View and manage reminders

1.  User opens New Reminder.
2.  User selects View Reminders.
3.  The management window opens.
4.  User can inspect reminders and perform supported actions: edit,
    delete, complete, and reschedule.
5.  Closing the management window returns the application to the
    background.

## 7. User interface requirements

The application should have two primary windows and a small system tray
menu.

### 7.1 New Reminder window

This is the default and most frequently used interface.

**Purpose:** Allow a user to create a reminder with minimal interaction.

**Required elements:**

-   Window title: New Reminder.
-   Reminder title text field.
-   Date selector.
-   Time selector.
-   Quick-time presets.
-   Separate natural-language text input area.
-   Create Reminder action.
-   View Reminders navigation action.
-   Clear validation and parsing feedback.

**Structured input:**

The user can enter a title, select a date, and select a time
independently.

**Quick-time presets:**

Initial suggested presets:

-   In 30 minutes.
-   In 1 hour.
-   In 2 hours.
-   Tomorrow.
-   Next week.

Presets are convenience actions. The user should still be able to adjust
the resulting date/time before saving.

**Natural-language input examples:**

-   "Remind me to review the paper tomorrow at 10 AM."
-   "Submit the internship report in 2 hours."
-   "Call the project mentor on 15 November at 4 PM."
-   "Finish the assignment in 3 days."

The parser should extract the task and schedule, then show a
confirmation/editing step.

**Design principles:**

-   Small, uncluttered window.
-   Fast to open and use.
-   No unnecessary dashboard elements.
-   Clear distinction between structured and natural-language input.
-   Accessible keyboard navigation where practical.
-   No requirement for an internet connection.

### 7.2 View Reminders window

**Purpose:** Provide a simple place to inspect and manage stored
reminders.

**Required sections:**

1.  **Upcoming:** Future pending reminders.
2.  **Overdue:** Pending reminders whose scheduled time has passed.
3.  **Completed:** Reminders explicitly marked Done.

**Required actions:**

-   Edit reminder title/date/time.
-   Delete reminder.
-   Mark reminder Done.
-   Reschedule reminder.

**Design principles:**

-   Prioritize readable reminder titles and scheduled times.
-   Clearly distinguish overdue and completed states.
-   Avoid turning the window into a full task-management dashboard.
-   Search, tags, categories, sorting options, and advanced filters are
    deferred unless needed after initial use.

### 7.3 Missed-reminder recovery window

**Purpose:** Surface reminders that became due while the application or
computer was unavailable.

Each overdue reminder should display:

-   Reminder title.
-   Original scheduled date and time.
-   Overdue duration, where practical.
-   Done action.
-   Reschedule action, with Snooze presets and a custom date/time (see 6.7).

Multiple overdue reminders should be manageable in one consolidated
interface.

### 7.4 System tray menu

The tray menu should provide a small set of actions:

-   New Reminder.
-   View Reminders.
-   Exit.

Clicking the tray icon should open New Reminder. The exact
single-click/double-click and context-menu behaviour should be
finalized during UI implementation.

### 7.5 Reminder alert window

**Purpose:** Deliver a due reminder in a way that does not depend on
Windows notification settings.

**Required elements:**

-   Reminder title and scheduled time.
-   **Done** action.
-   **Reschedule** action, opening the Snooze presets and a custom
    date/time option (see 6.7).
-   A consolidated list when several reminders are due together.

**Behaviour:**

-   Appears above other windows when a reminder falls due.
-   Remains until the user acts; closing it without an action leaves the
    reminder pending and overdue.
-   The same window design is used for the missed-reminder recovery
    interface (7.3), so due and overdue reminders are handled in one
    place.
-   Small and uncluttered, in keeping with the rest of the interface.

## 8. Functional requirements

Requirements are grouped by capability. "Must" indicates a
release-blocking requirement for v1.0; "Should" indicates a desirable
requirement that may be adjusted if implementation constraints require
it.

### 8.1 Reminder creation and input

-   **FR-01 (Must):** The user can create a reminder with a title, date,
    and time.
-   **FR-02 (Must):** The user can create a reminder using a
    natural-language sentence.
-   **FR-03 (Must):** Natural-language parsing runs locally without a
    remote API.
-   **FR-04 (Must):** Parsed title and schedule are shown for
    confirmation before saving.
-   **FR-05 (Must):** The user can correct parsed values.
-   **FR-06 (Must):** The application validates missing, invalid, past,
    and ambiguous date/time inputs.
-   **FR-07 (Should):** Quick-time presets are available for common
    relative schedules.

### 8.2 Reminder management

-   **FR-08 (Must):** Reminders are stored persistently in a local
    database.
-   **FR-09 (Must):** The user can view upcoming, overdue, and completed
    reminders.
-   **FR-10 (Must):** The user can edit a reminder.
-   **FR-11 (Must):** The user can delete a reminder.
-   **FR-12 (Must):** The user can mark a reminder as Done.
-   **FR-13 (Must):** The user can reschedule a reminder, either with a
    Snooze preset or by choosing a specific date and time.
-   **FR-14 (Must):** A reminder remains pending after its due time
    until the user explicitly changes its state.
-   **FR-15 (Should):** The application records basic completion and
    rescheduling history.

### 8.3 Notifications and scheduling

-   **FR-16 (Must):** When a reminder is due and the application is
    running, RemindMe shows its application-owned alert window (see
    FR-37 to FR-41). A Windows notification may accompany it.
-   **FR-17 (Must):** The scheduler is updated after reminders are
    created, edited, deleted, completed, or rescheduled.
-   **FR-18 (Must):** Future reminders are restored from persistent
    storage after application restart.
-   **FR-19 (Must):** The application reconciles pending reminders on
    startup.
-   **FR-20 (Must):** The application reconciles pending reminders after
    system resume from sleep.
-   **FR-21 (Must):** Overdue reminders are presented for recovery.
-   **FR-22 (Must):** Multiple overdue reminders are handled in a
    consolidated and controlled way.
-   **FR-23 (Should):** Activating a Windows notification brings the
    relevant alert or reminder to the front.
-   **FR-24 (Later):** Native toast action buttons for Done and
    Reschedule may be added after the core workflow is stable. They are
    not required, because the alert window already provides these
    actions.

### 8.4 Application lifecycle

-   **FR-25 (Must):** The application can start automatically after the
    current Windows user logs in.
-   **FR-26 (Must):** Closing application windows does not terminate the
    background process.
-   **FR-27 (Must):** The user can explicitly exit through the tray
    menu.
-   **FR-28 (Must):** The hotkey, the desktop shortcut, and the tray icon
    each open New Reminder.
-   **FR-29 (Must):** Clicking the shortcut while the application is
    already running activates the existing instance.
-   **FR-30 (Must):** The application prevents accidental duplicate
    instances.
-   **FR-31 (Must):** The application runs without administrator
privileges.

### 8.5 Global hotkey

-   **FR-32 (Must):** A global hotkey opens New Reminder from any
    application while RemindMe is running.
-   **FR-33 (Must):** The hotkey is registered with the Windows hotkey
    API and released when the application exits; no global keyboard
    hook is used.
-   **FR-34 (Must):** If the hotkey cannot be registered, the application
    continues to run, informs the user, and keeps the tray and shortcut
    paths working.
-   **FR-35 (Should):** The user can change the hotkey through a simple
    setting.
-   **FR-36 (Must):** Pressing the hotkey while New Reminder is open
    focuses the existing window.

### 8.6 Alerts and rescheduling

-   **FR-37 (Must):** A due reminder is shown in an application-owned
    alert window with its title, scheduled time, Done, and Reschedule.
-   **FR-38 (Must):** The alert is shown regardless of Windows
    notification or Focus Assist settings.
-   **FR-39 (Must):** The alert remains until the user acts; closing it
    without an action leaves the reminder pending and overdue.
-   **FR-40 (Must):** Reminders that are due together are shown in one
    consolidated alert.
-   **FR-41 (Must):** Reschedule offers Snooze presets and a custom
    date/time; Snooze is not a separate top-level action.
-   **FR-42 (Should):** A Windows notification accompanies the alert as
    an attention aid; failure to show it does not affect the alert.

### 8.7 Installation

-   **FR-43 (Must):** A per-user Inno Setup installer installs the
    application without administrator privileges.
-   **FR-44 (Must):** The installer creates a Start Menu shortcut,
    offers a desktop shortcut, and offers startup-at-login
    registration.
-   **FR-45 (Must):** The uninstaller removes the application and its
    startup registration, and does not delete user reminder data without
    asking.
-   **FR-46 (Must):** Upgrading to a newer version preserves the existing
    reminder database.

## 9. Reminder state and lifecycle rules

The reminder lifecycle must be explicit and predictable.

### 9.1 Core states

-   **Pending:** Reminder is active and has not been completed or
    deleted. It may be upcoming or overdue.
-   **Completed:** User explicitly marked the reminder Done.
-   **Deleted:** User explicitly deleted the reminder. Whether deletion
    is physical or represented by a soft-delete state is a low-level
    design decision.

Overdue is best treated as a time-derived condition of a Pending
reminder, rather than a separate terminal state.

### 9.2 State rules

-   Passing the scheduled time does not complete a reminder.
-   A missed reminder remains Pending.
-   Rescheduling updates the scheduled time and keeps the reminder
    Pending.
-   Completing a reminder records a completion timestamp.
-   Editing a completed reminder should not silently reactivate it; the
    final UI behaviour should be specified during detailed design.
-   Deleting a reminder removes it from active reminder views.
-   A reminder must not be delivered repeatedly merely because the
    scheduler recalculates its next due time.
-   Startup/resume reconciliation must be safe to run more than once.

### 9.3 Time handling

-   The application must use a consistent timestamp strategy internally.
-   Store timestamps in a timezone-safe format; UTC storage with
    local-time display is recommended.
-   Display dates and times in the user's local timezone.
-   Validate ambiguous and nonexistent local times where daylight-saving
    transitions apply.
-   Reconcile reminders against the current system time after startup
    and resume.
-   The final low-level design must define behaviour when the user
    changes the Windows timezone or system clock.

## 10. Non-functional requirements

### 10.1 Performance and resource efficiency

RemindMe is expected to run in the background for long periods. Low idle
resource consumption is therefore a core engineering requirement.

**Proposed optimization targets (to be measured and validated):**

  -----------------------------------------------------------------------
  Metric                                                   Initial target
  ------------------------------ ----------------------------------------
  Background RAM usage                                Aim for under 50 MB

  Idle CPU usage                              Near 0% when no work is due

  Quick-add window opening                           Aim for under 500 ms

  Network activity at runtime                                        None

  Background scheduling                       Event-driven; no continuous
                                                   high-frequency polling
  -----------------------------------------------------------------------

These are engineering targets, not measured results or guarantees.
Actual memory usage depends on Python, Qt, packaging, Windows version,
loaded modules, and notification integration. If the 50 MB target
conflicts with reliability or maintainability, prioritize stable
behaviour and low idle CPU, then document measured usage honestly.

**Optimization principles:**

-   Create the QApplication and system tray integration at startup, but
    instantiate GUI windows only when needed.
-   Avoid loading the natural-language parser until natural-language
    input is used, if practical.
-   Avoid unnecessary background threads and worker processes.
-   Avoid continuous database polling.
-   Use an event-driven scheduler based on the next pending reminder.
-   Use one-shot timers and recalculate the next due reminder after
    relevant events.
-   Keep the dependency set small.
-   Avoid browser engines, web views, animations, and heavyweight UI
    frameworks.
-   Keep database queries indexed and focused.
-   Measure packaged application performance rather than estimating from
    development mode alone.
-   Package as a PyInstaller one-directory build (decided; see 11.3) and
    measure its startup and memory use.

### 10.2 Reliability

-   Reminder data must survive application restarts and Windows
    restarts.
-   A crash must not silently erase reminders.
-   Database writes should use transactions.
-   Startup and resume reconciliation must be idempotent.
-   The application must not create duplicate notifications for the same
    due event during normal operation.
-   Errors should be handled without silently discarding pending
    reminders.
-   The application should recover gracefully from a missing, locked, or
    temporarily inaccessible database.
-   The exact notification delivery guarantees and retry policy must be
    defined during low-level design.

**Important platform limitation:** Windows cannot display an application
notification while the laptop is powered off. During sleep, delivery may
also be delayed. RemindMe must recover overdue reminders when Windows
resumes or starts and the application gets an opportunity to execute. It
must not claim to notify while the machine is unavailable.

### 10.3 Usability

-   The primary reminder creation workflow should be short and
    understandable.
-   The default entry point should be New Reminder, not a dashboard.
-   Structured and natural-language input should both be available.
-   Parsing failures should be explained clearly.
-   Users should be able to correct parsed information before saving.
-   Done and Reschedule should be distinct actions.
-   The product should use consistent terminology: the action is
    Reschedule, and Snooze is only the label of the quick-delay presets
    within it.
-   Overdue reminders should be visually distinguishable from upcoming
    reminders.

### 10.4 Portability and compatibility

-   Initial target is supported Windows desktop versions selected during
    implementation.
-   The application should run as a normal user.
-   The executable should not require a separately installed Python
    runtime.
-   Application data should be stored in the current user's local
    application-data directory.
-   The application should avoid relying on the executable's
    installation directory for writable data.
-   Windows startup and notification integration should be tested on
    clean Windows installations.

### 10.5 Maintainability and testability

-   Separate UI, reminder logic, storage, parsing, scheduling, and
    Windows integration.
-   Keep platform-specific code isolated.
-   Provide automated tests for date parsing, state transitions,
    persistence, and recovery logic.
-   Keep dependencies minimal and version-pinned.
-   Document build and release procedures.
-   Make the application straightforward for external contributors to
    build and test.

## 11. Proposed technology stack (frozen initial choice)

The following is the agreed initial stack. It should be treated as the
default implementation direction unless a concrete technical limitation
is discovered during prototyping.

| Layer | Technology | Responsibility |
|---|---|---|
| Programming language | Python | Application implementation |
| Desktop GUI | PySide6 / Qt Widgets (LGPLv3; see 12.6) | New Reminder, View Reminders, alert and recovery windows |
| Local database | Python `sqlite3` / SQLite | Persistent reminder storage |
| Scheduling | Qt event loop and one-shot `QTimer` | Trigger the next due reminder |
| Natural-language date parsing | `dateparser` plus custom preprocessing and validation | Extract date/time expressions from user input |
| Due-reminder delivery | Application-owned alert window (Qt Widgets) | Primary delivery with Done and Reschedule |
| Windows notifications | Native Windows toast integration | Supplementary attention aid |
| Global hotkey | Windows `RegisterHotKey` through a Qt native event filter | Open New Reminder from anywhere |
| System tray | Qt `QSystemTrayIcon` | Tray icon and menu |
| Startup integration | Per-user startup registration, offered by the installer | Launch after user login |
| Single-instance handling | `QLockFile` and/or `QLocalServer` | Prevent duplicate processes and activate the existing one |
| Packaging | PyInstaller `--onedir` | Produce the application directory |
| Installer | Inno Setup (per-user, no administrator) | Install, shortcuts, startup option, upgrade, uninstall |
| Code signing | SignPath Foundation (planned after first public release) | Sign the executable and installer |
| Source hosting and releases | GitHub, GitHub Releases | Repository, installer download, checksums |

### 11.1 Scheduling design choice

Use the Qt event loop and one-shot `QTimer` rather than introducing
APScheduler for the initial version.

Expected approach:

1.  Query SQLite for the earliest pending reminder.
2.  Calculate the delay until it is due.
3.  Set a one-shot timer.
4.  When it fires, process due reminders.
5.  Re-query for the next pending reminder and schedule again.
6.  Reconcile from SQLite on startup and system resume.

SQLite remains the source of truth. The timer is only a mechanism for
waking the application at the next relevant time. It must not be the
only place where reminder state exists.

### 11.2 Natural-language parser design choice

Use a deterministic, local parser rather than an LLM.

The parser should:

-   Identify date/time expressions.
-   Extract or preserve the task description.
-   Support relative expressions such as "in 30 minutes," "in 2 hours,"
    and "in 3 days."
-   Support absolute expressions such as "tomorrow at 9 AM" and "15
    November at 4 PM."
-   Validate ambiguous or incomplete expressions.
-   Present extracted values for confirmation.
-   Fall back to structured input when interpretation is uncertain.

The exact parsing strategy and supported language grammar will be
specified during low-level design and testing.

### 11.3 Packaging and installation (decided)

The distribution pipeline is **PyInstaller `--onedir` + Inno Setup +
GitHub Releases**.

-   PyInstaller one-directory mode is used instead of one-file. One-file
    builds unpack to a temporary directory on every launch, which slows
    startup (relevant to the 500 ms target and to login startup) and
    tends to attract more antivirus false positives. One-directory also
    keeps the Qt libraries as separate files, which suits the LGPL
    requirements in 12.6.
-   Inno Setup produces a **per-user installer** that does not require
    administrator privileges (`PrivilegesRequired=lowest`).
-   The installer creates a Start Menu shortcut (also needed for Windows
    notification integration), offers a desktop shortcut, and offers
    startup at login.
-   The uninstaller removes the program and startup registration. User
    data in `%LOCALAPPDATA%\RemindMe\` is kept unless the user chooses to
    remove it.
-   Upgrades keep the existing database; schema migrations are handled
    by the application, not the installer.
-   The release artifact is the installer, published to GitHub Releases
    with a SHA-256 checksum and built from a tagged commit in GitHub
    Actions.
-   A portable ZIP of the one-directory build may be offered later.

## 12. Security and privacy requirements

RemindMe is intended to be local-only and offline-first. This reduces
the attack surface but does not eliminate risks from dependencies, local
data handling, or distributed executable files.

### 12.1 Runtime privacy

-   No internet connection should be required for normal operation.
-   No telemetry or analytics.
-   No remote API calls.
-   No cloud synchronization.
-   No user accounts or authentication.
-   No transmission of reminder titles, schedules, or other user data.
-   Reminder data should remain on the user's device.
-   Logs should avoid recording reminder text unless explicitly needed
    for a user-facing diagnostic and controlled by the user.

### 12.2 Local application security

-   Run with standard user privileges; do not request administrator
    access.
-   Store the database and application data under the user's local
    application-data directory, for example
    `%LOCALAPPDATA%\\RemindMe\\`.
-   Do not store writable application data beside the executable.
-   Use parameterized SQL queries for all user-controlled database
    values.
-   Never use `eval`, `exec`, or shell execution to interpret reminder
    text.
-   Treat natural-language input as untrusted plain text.
-   Validate and normalize file paths.
-   Avoid unnecessary file-system access.
-   Use SQLite transactions and appropriate database error handling.
-   Keep logs free of unnecessary personal information.
-   Consider local database backup and recovery behaviour.
-   Do not claim encryption at rest unless it is actually implemented
    and its key-management model is defined.

### 12.3 Dependency and supply-chain security

-   Keep the dependency set as small as practical.
-   Pin dependency versions.
-   Maintain a reproducible dependency specification or lockfile.
-   Review dependencies and their licenses before inclusion.
-   Use dependency vulnerability checks as part of release preparation.
-   Avoid installing or executing dependencies dynamically at runtime.
-   Review updates before upgrading dependencies.

### 12.4 GitHub release security

Publishing an executable introduces risks even if the application itself
is offline.

Required release practices:

-   Publish releases only from the official repository.
-   Build release artifacts from identifiable source tags or commits.
-   Provide SHA-256 checksums for downloadable binaries.
-   Keep release notes and source revisions traceable.
-   Use least-privilege GitHub Actions permissions.
-   Pin third-party GitHub Actions to full commit SHAs where practical.
-   Avoid unnecessary secrets in build workflows.
-   Do not silently download and execute updates.
-   Apply to the **SignPath Foundation** for free code signing for open
    source once the project has a public release. Check the current
    eligibility conditions at application time; at the time of writing
    they include an OSI-approved license, a public repository, no
    proprietary components in signed packages, multi-factor
    authentication for team members, and a published code-signing
    policy. Signed builds must come from the public CI pipeline.
-   Until signing is in place, document that the unsigned installer may
    trigger Windows SmartScreen or antivirus reputation warnings, and
    point users to the checksum.

A checksum helps verify that a downloaded file matches the published
artifact; it does not independently prove that the artifact is benign.
Code signing can help establish publisher identity and detect
modifications, but it is not a substitute for secure build practices.

### 12.5 Notification privacy

Windows may retain notification content in its own notification history.
Deleting a reminder from RemindMe does not necessarily remove previously
displayed notification content from Windows. This behaviour should be
documented.

### 12.6 Third-party licensing (PySide6 and other dependencies)

PySide6 (Qt for Python) is offered under the LGPLv3, the GPLv3, or a
commercial license from The Qt Company. RemindMe uses it under the
**LGPLv3**, which permits use in open-source and closed-source
applications provided the following are respected. This is a
planning summary, not legal advice.

-   Use only Qt modules that are available under LGPLv3 (the core, GUI,
    and Widgets modules RemindMe needs). Some Qt add-on modules are
    available only under GPLv3 or a commercial license and must not be
    included unless the project license is chosen accordingly.
-   Link dynamically. The PyInstaller one-directory build keeps PySide6
    and the Qt libraries as separate files, so users can replace them.
-   Ship the LGPLv3 license text and Qt/PySide6 copyright notices with the
    installer, for example in a `THIRD_PARTY_NOTICES` file.
-   Make the corresponding PySide6/Qt source available, for example by
    linking to the exact upstream release used.
-   Do not add terms that prohibit modifying the application for the
    user's own use or reverse engineering for debugging such
    modifications.
-   Exclude unused Qt modules from the build to reduce size and licensing
    surface.
-   Choose and publish the project's own license in the repository
    before the first public release, and make sure it is OSI-approved
    (required by SignPath Foundation). Review the licenses of every
    other dependency (for example `dateparser`) and record them in
    `THIRD_PARTY_NOTICES`.

## 13. MVP scope --- version 1.0

The first public release should focus on the smallest complete and
dependable reminder lifecycle.

### 13.1 Included in v1.0

**Application and access**

-   Windows desktop application with a per-user Inno Setup installer.
-   Global hotkey, desktop/Start Menu shortcut, and system tray icon.
-   Startup after user login (installer option).
-   Single-instance behaviour.
-   Background operation after windows close.
-   Explicit Exit action.

**Creation**

-   New Reminder window.
-   Structured title, date, and time fields.
-   Quick-time presets.
-   Natural-language input in its own input area.
-   Local date/time parsing.
-   Parsed-value confirmation and correction.
-   Input validation.

**Management**

-   View Reminders window.
-   Upcoming, overdue, and completed sections.
-   Edit reminder.
-   Delete reminder.
-   Mark Done.
-   Reschedule, with Snooze presets or a user-selected date/time.

**Scheduling, alerts, and recovery**

-   Persistent SQLite storage.
-   Event-driven scheduling.
-   Application-owned alert window with Done and Reschedule.
-   Supplementary Windows notifications.
-   Startup reconciliation.
-   Resume-from-sleep reconciliation.
-   Missed-reminder recovery interface.
-   Consolidated handling of multiple due or overdue reminders.
-   No automatic completion of overdue reminders.

**Quality and distribution**

-   Basic automated tests.
-   Resource and startup profiling.
-   Security, dependency, and license review.
-   PyInstaller one-directory build packaged with Inno Setup.
-   GitHub release with installer, checksum, and build instructions.

### 13.2 Explicitly excluded from v1.0

-   Cloud sync.
-   Accounts and authentication.
-   Calendar integration.
-   Mobile companion app.
-   AI/LLM parsing.
-   Recurring reminders unless implementation proves trivial and
    reliable.
-   Categories, tags, and project boards.
-   Productivity analytics.
-   Full alarm-clock mode.
-   Automatic online updates.
-   Native notification action buttons if they materially delay the
    reliable core workflow.

## 14. Future enhancements

Potential post-v1.0 improvements, to be prioritized based on actual
usage:

-   Recurring reminders.
-   Categories or tags.
-   Search, sorting, and advanced filtering.
-   Import/export and user-controlled backups.
-   Custom notification sounds.
-   Optional persistent alert mode for selected reminders.
-   Native Windows notification actions.
-   Hotkey customization interface.
-   Optional portable mode.
-   Accessibility and keyboard-shortcut improvements.
-   More natural-language expressions and locale support.

These are not commitments for the first release.

## 15. Testing and acceptance criteria

The first release should not be considered complete merely because the
UI works. The reminder lifecycle must be tested under realistic
operating conditions.

### 15.1 Functional acceptance tests

-   Create a reminder using structured fields.
-   Create a reminder using natural-language input.
-   Correct a parser result before saving.
-   Reject or request clarification for ambiguous input.
-   Edit a pending reminder.
-   Delete a pending reminder.
-   Mark a reminder Done.
-   Reschedule an overdue reminder.
-   Verify that completed reminders do not reappear as pending.
-   Verify that reminders persist after application restart.
-   Verify that reminders persist after Windows restart.
-   Open New Reminder with the hotkey from another application.
-   Install, upgrade, and uninstall with the installer, confirming the
    database survives an upgrade.

### 15.2 Reliability scenarios

-   Reminder becomes due while the application is running.
-   Reminder becomes due while the application window is closed but the
    background process is running.
-   Reminder becomes due while the laptop sleeps.
-   Reminder becomes due while the laptop is shut down.
-   Application is manually terminated before the due time.
-   Multiple reminders become overdue during shutdown.
-   System resumes after several hours.
-   Application starts after multiple days of missed reminders.
-   System clock or timezone changes.
-   Database is temporarily inaccessible or encounters an error.
-   Application is launched twice.
-   Hotkey is already registered by another application.
-   Reminder becomes due while Focus Assist / Do Not Disturb is on.
-   Alert is closed without choosing Done or Reschedule.

Expected result: pending reminders must be recovered or surfaced
according to their stored schedule and current system time. The
application must not silently discard them or mark them completed.

### 15.3 Performance acceptance

Measure on a documented Windows test environment:

-   Idle RAM usage after startup and stabilization.
-   RAM usage while New Reminder is open.
-   RAM usage while View Reminders is open.
-   Idle CPU usage over a representative period.
-   Startup-to-ready time.
-   Time to open New Reminder from the tray and desktop shortcut.
-   Behaviour with a larger reminder database.
-   Resource usage of the packaged executable, not just the development
    process.

The initial target is under 50 MB of background RAM, near-zero idle CPU,
and a quick-add opening time below 500 ms. Report actual measurements
and test conditions in release documentation; do not claim targets were
met without measurements.

### 15.4 Security acceptance

-   No runtime network requests during normal operation.
-   No unnecessary administrator privileges.
-   No dynamic execution of reminder input.
-   Parameterized SQL for user-controlled values.
-   Dependencies reviewed and pinned.
-   Release checksum generated and verified.
-   Build workflow permissions reviewed.
-   No secrets embedded in the executable or repository.
-   Application data stored in the user's local application-data
    directory.
-   No reminder content unnecessarily written to logs.

## 16. Known constraints and engineering caveats

1.  **Power-off limitation:** No desktop application can display a
    notification while the laptop is powered off. RemindMe must recover
    the reminder after the next startup.
2.  **Sleep limitation:** Notification delivery may be delayed while
    Windows sleeps. Recovery must occur on resume.
3.  **Background process dependency:** If the application is explicitly
    exited, it cannot deliver notifications until it is launched again.
    Startup and manual launch must reconcile overdue reminders.
4.  **Windows notification behaviour:** Native notification
    registration, activation, and interactive actions may require
    Windows-specific integration beyond a basic Qt tray message.
5.  **Unsigned executable warnings:** GitHub-distributed unsigned
    executables may trigger SmartScreen or antivirus reputation
    warnings.
6.  **Resource targets:** PySide6 and Python have a runtime baseline.
    The proposed RAM target must be validated empirically.
7.  **Date/time ambiguity:** Natural-language date parsing is not always
    unambiguous. Confirmation and structured correction are required.
8.  **System clock changes:** The scheduler must recalculate after
    relevant clock/timezone changes where feasible.
9.  **Notification history:** Windows may retain notification content
independently of the application's database.
10. **Hotkey conflicts:** Another application may already own the chosen
    hotkey, and some key combinations behave differently on some
    keyboard layouts.
11. **Notification suppression:** Windows toasts can be suppressed or
    missed, which is why the application-owned alert is the primary
    delivery mechanism.
12. **Licensing:** PySide6 is used under the LGPLv3; the obligations in
    12.6 apply to every release.

## 17. Initial release success criteria

RemindMe v1.0 will be successful if a user can:

1.  Open a small New Reminder window with a hotkey, or from the desktop
    or system tray in a few clicks.
2.  Create a reminder using either structured fields or natural
    language.
3.  Close the window while the application continues running in the
    background.
4.  See an alert when a reminder is due and Windows is running, even if
    notifications are suppressed.
5.  See and manage upcoming, overdue, and completed reminders.
6.  Mark a task Done or choose a new time through Reschedule.
7.  Recover reminders missed during sleep, shutdown, or application
    unavailability.
8.  Restart Windows without losing pending reminders.
9.  Use the application without an internet connection or account.
10. Download the installer from the official GitHub release and install
    it without administrator privileges.

The product should remain small, dependable, private, and easy to use. A
successful first release is not the one with the most features; it is
the one that reliably solves the original reminder problem without
creating another complicated system the user has to manage.

------------------------------------------------------------------------

## Appendix A --- Decisions agreed so far

| Topic | Agreed direction |
|---|---|
| Product | Lightweight personal reminder application |
| Platform | Windows desktop only |
| Distribution | Open-source GitHub repository; PyInstaller `--onedir` + Inno Setup installer through GitHub Releases |
| Code signing | Apply to SignPath Foundation after the first public release |
| Default entry point | New Reminder window |
| Global hotkey | Enabled; opens New Reminder from anywhere |
| Desktop shortcut | Opens New Reminder |
| Tray icon | Opens New Reminder |
| Management interface | Separate View Reminders window |
| Creation methods | Structured fields and natural-language input, kept as two separate input areas |
| Natural-language processing | Local deterministic parser; no LLM/API |
| Due-reminder delivery | Application-owned alert window with Done and Reschedule; Windows toast is supplementary |
| Background operation | Starts after Windows login; remains active after windows close |
| Persistence | Local SQLite database |
| Missed reminders | Recover after startup/resume |
| Overdue actions | Done and Reschedule |
| Snooze terminology | "Snooze" labels the quick-delay presets inside Reschedule; it is not a separate action |
| Scheduling approach | Qt event loop and one-shot QTimer |
| GUI | PySide6 / Qt Widgets, used under LGPLv3 |
| Packaging | PyInstaller `--onedir` |
| Network | No runtime internet dependency |
| Security posture | Least privilege, minimal dependencies, local data, secure release practices |
| Performance goal | Aim for under 50 MB idle/background RAM and near-zero idle CPU; measure empirically |

## Appendix B --- Items reserved for low-level design

The product scope is established, but the following implementation
details are intentionally not finalized in this document:

-   Exact Python package/module structure.
-   Class responsibilities and interfaces.
-   Detailed SQLite schema, indexes, migrations, and deletion policy.
-   Exact reminder state-transition implementation.
-   Parser grammar, supported locales, and ambiguity thresholds.
-   Windows notification registration and activation mechanism.
-   System resume and system clock-change event handling.
-   Startup registration mechanism and uninstall cleanup.
-   Single-instance activation protocol.
-   Recovery batching and notification retry policy.
-   Exact keyboard shortcuts and window placement behaviour.
-   Automated test architecture and CI workflow.
-   Default hotkey combination, conflict handling, and the setting used to
    change it.
-   Alert window behaviour: focus handling, stacking, and appearance over
    full-screen applications.
-   Final Snooze preset list.
-   Inno Setup script details: startup option, shortcut and Windows
    notification identity, upgrade and uninstall behaviour.
-   Project license choice and `THIRD_PARTY_NOTICES` contents.
-   SignPath Foundation application timing and signing workflow in
    GitHub Actions.

These should be resolved in the low-level design before implementation
begins.
