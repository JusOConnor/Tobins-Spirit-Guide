// The web page for Tobin's Spirit Guide.
//
// This file builds the evidence rows and ghost rows, responds to your taps,
// runs the timer, keeps the screen awake, and remembers your choices.
// The rules themselves live in logic.js, which loads before this file.


// Where the ghost list lives, relative to index.html.
const GHOST_DATA_PATH = 'functions/ghost_data.json';

// The name your choices are saved under in this browser.
const SAVED_CHOICES_KEY = 'tobins_spirit_guide_selections';

// The style class used to color a ghost row for each result.
const STATUS_CLASSES = {
    [CONFIRMED]: 'status_confirmed',
    [TWO_FOUND]: 'status_two_found',
    [ONE_FOUND]: 'status_one_found',
    [OPEN]: 'status_open',
    [ELIMINATED]: 'status_eliminated',
};

// The style class used to color an evidence button for each choice.
const CHOICE_CLASSES = {
    [RULED_OUT]: 'choice_ruled_out',
    [UNKNOWN]: 'choice_unknown',
    [FOUND]: 'choice_found',
};


// Everything the page needs to remember while it is open.
const state = {
    ghosts: [],
    evidenceTypes: [],
    selections: {},
    evidenceButtons: {},   // evidence name, then choice, then its button
    ghostRows: {},         // ghost name, then the parts of its row
    openGhostName: null,   // the ghost whose details are showing, if any
    timerInterval: null,
    timerEndTime: null,
    wakeLock: null,
};


// Starting the page

async function startPage() {
    try {
        state.ghosts = await loadGhosts();
    } catch (error) {
        showLoadError();
        return;
    }

    state.evidenceTypes = getEvidenceTypes(state.ghosts);
    state.selections = loadSavedChoices();

    buildEvidenceList();
    buildGhostList();
    connectButtons();
    refresh();

    keepScreenAwake();
    registerOfflineSupport();
}


async function loadGhosts() {
    const response = await fetch(GHOST_DATA_PATH);
    if (!response.ok) {
        throw new Error(`Could not load ${GHOST_DATA_PATH}`);
    }
    return response.json();
}


function showLoadError() {
    const message = document.getElementById('load_error');
    message.textContent = 'The ghost list could not be loaded. Check your connection and refresh the page.';
    message.hidden = false;
}


// Building the evidence rows

function buildEvidenceList() {
    const list = document.getElementById('evidence_list');

    for (const evidence of state.evidenceTypes) {
        const row = document.createElement('div');
        row.className = 'evidence_row';

        const label = document.createElement('span');
        label.className = 'evidence_name';
        label.textContent = evidence;
        row.append(label);

        // Three buttons side by side that act as a single choice.
        const choiceGroup = document.createElement('div');
        choiceGroup.className = 'choice_group';
        choiceGroup.setAttribute('role', 'group');
        choiceGroup.setAttribute('aria-label', evidence);

        state.evidenceButtons[evidence] = {};

        for (const choice of EVIDENCE_CHOICES) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'choice_button';
            button.textContent = choice;
            button.addEventListener('click', () => chooseEvidence(evidence, choice));
            choiceGroup.append(button);
            state.evidenceButtons[evidence][choice] = button;
        }

        row.append(choiceGroup);
        list.append(row);
    }
}


// Building the ghost rows

function buildGhostList() {
    const list = document.getElementById('ghost_list');

    for (const ghost of state.ghosts) {
        const row = document.createElement('div');
        row.className = 'ghost_row';

        const nameButton = document.createElement('button');
        nameButton.type = 'button';
        nameButton.className = 'ghost_name';
        nameButton.textContent = ghost.name;
        nameButton.setAttribute('aria-expanded', 'false');
        nameButton.addEventListener('click', () => toggleDetails(ghost.name));
        row.append(nameButton);

        const chips = [];
        for (const evidence of ghost.evidence) {
            const chip = document.createElement('span');
            chip.className = 'evidence_chip';
            chip.textContent = evidence;
            row.append(chip);
            chips.push(chip);
        }

        // The details row sits right under its ghost and stays hidden until tapped.
        const details = document.createElement('div');
        details.className = 'ghost_details';
        details.hidden = true;

        const strength = document.createElement('p');
        strength.innerHTML = '<strong>Strength:</strong> ';
        strength.append(ghost.strength);

        const weakness = document.createElement('p');
        weakness.innerHTML = '<strong>Weakness:</strong> ';
        weakness.append(ghost.weakness);

        details.append(strength, weakness);

        list.append(row, details);
        state.ghostRows[ghost.name] = { row, nameButton, chips, details };
    }
}


// Responding to your taps

function chooseEvidence(evidence, choice) {
    state.selections[evidence] = choice;
    refresh();
}


function resetEvidence() {
    state.selections = newSelections(state.evidenceTypes);
    refresh();
}


function toggleDetails(ghostName) {
    // Close whichever ghost is open, then open the tapped one
    // unless it was the one already open.
    const wasOpen = state.openGhostName === ghostName;

    if (state.openGhostName !== null) {
        setDetailsOpen(state.openGhostName, false);
        state.openGhostName = null;
    }

    if (!wasOpen) {
        setDetailsOpen(ghostName, true);
        state.openGhostName = ghostName;
    }
}


function setDetailsOpen(ghostName, isOpen) {
    const parts = state.ghostRows[ghostName];
    parts.details.hidden = !isOpen;
    parts.nameButton.setAttribute('aria-expanded', String(isOpen));
    parts.row.classList.toggle('is_open', isOpen);
}


// Recolor every evidence button and ghost row to match your choices.
function refresh() {
    for (const evidence of state.evidenceTypes) {
        const selected = state.selections[evidence];

        for (const [choice, button] of Object.entries(state.evidenceButtons[evidence])) {
            const isSelected = choice === selected;
            button.classList.remove(...Object.values(CHOICE_CLASSES));
            if (isSelected) {
                button.classList.add(CHOICE_CLASSES[choice]);
            }
            button.setAttribute('aria-pressed', String(isSelected));
        }
    }

    for (const ghost of state.ghosts) {
        const status = ghostStatus(ghost, state.selections);
        const parts = state.ghostRows[ghost.name];

        parts.row.classList.remove(...Object.values(STATUS_CLASSES));
        parts.row.classList.add(STATUS_CLASSES[status]);

        // With two pieces found, light up the last piece still to look for.
        let stillNeeded = [];
        if (status === TWO_FOUND) {
            stillNeeded = remainingEvidence(ghost, state.selections);
        }

        ghost.evidence.forEach((evidence, position) => {
            const chip = parts.chips[position];
            chip.classList.toggle('is_needed', stillNeeded.includes(evidence));
        });
    }

    saveChoices();
}


function connectButtons() {
    document.getElementById('reset_button').addEventListener('click', resetEvidence);
    document.getElementById('timer_two').addEventListener('click', () => startTimer(2 * 60));
    document.getElementById('timer_five').addEventListener('click', () => startTimer(5 * 60));
    document.getElementById('timer_stop').addEventListener('click', stopTimer);
}


// Remembering your choices

function saveChoices() {
    // Some private browsing modes block saving, so a failure here is ignored.
    try {
        localStorage.setItem(SAVED_CHOICES_KEY, JSON.stringify(state.selections));
    } catch (error) {
        // Nothing to do; the page still works, it just won't remember.
    }
}


function loadSavedChoices() {
    const selections = newSelections(state.evidenceTypes);

    try {
        const saved = JSON.parse(localStorage.getItem(SAVED_CHOICES_KEY) ?? '{}');

        // Only keep saved choices that still make sense, in case the
        // ghost list has changed since they were saved.
        for (const evidence of state.evidenceTypes) {
            if (EVIDENCE_CHOICES.includes(saved[evidence])) {
                selections[evidence] = saved[evidence];
            }
        }
    } catch (error) {
        // Start fresh if the saved choices can't be read.
    }

    return selections;
}


// The timer
//
// Rather than counting ticks, the timer remembers the moment it should reach
// zero and checks the real clock. That keeps it accurate even when a phone
// slows the page down in the background.

function startTimer(seconds) {
    // Clear any timer already running so two never tick at once.
    clearInterval(state.timerInterval);
    state.timerEndTime = Date.now() + seconds * 1000;
    updateTimer();
    state.timerInterval = setInterval(updateTimer, 250);
}


function updateTimer() {
    const readout = document.getElementById('timer_readout');
    const millisecondsLeft = state.timerEndTime - Date.now();

    if (millisecondsLeft > 0) {
        readout.textContent = formatTime(Math.ceil(millisecondsLeft / 1000));
        readout.classList.remove('is_overtime');
    } else {
        // Past zero, keep counting up in red to show how long it has been.
        readout.textContent = formatTime(Math.floor(-millisecondsLeft / 1000));
        readout.classList.add('is_overtime');
    }
}


function stopTimer() {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
    const readout = document.getElementById('timer_readout');
    readout.textContent = formatTime(0);
    readout.classList.remove('is_overtime');
}


// Keeping the screen awake
//
// Browsers let go of this whenever the page is hidden, such as switching apps,
// so it is asked for again each time the page comes back into view.

async function keepScreenAwake() {
    if (!('wakeLock' in navigator)) {
        setAwakeStatus('This browser cannot keep the screen awake.');
        return;
    }

    await requestWakeLock();

    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            requestWakeLock();
        }
    });

    // Some browsers only allow it after a tap, so try again on the first one.
    document.addEventListener('click', () => {
        if (state.wakeLock === null) {
            requestWakeLock();
        }
    });
}


async function requestWakeLock() {
    try {
        state.wakeLock = await navigator.wakeLock.request('screen');
        setAwakeStatus('Screen will stay awake');
        state.wakeLock.addEventListener('release', () => {
            state.wakeLock = null;
        });
    } catch (error) {
        state.wakeLock = null;
        setAwakeStatus('Tap anywhere to keep the screen awake');
    }
}


function setAwakeStatus(message) {
    document.getElementById('awake_status').textContent = message;
}


// Working without internet

function registerOfflineSupport() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service_worker.js').catch(() => {
            // The page still works online if this fails.
        });
    }
}


startPage();
