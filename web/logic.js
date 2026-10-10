// The rules of the guide: how your evidence narrows down the ghost.
//
// This file matches functions/logic.py rule for rule, so the web page and the
// desktop app always agree. If you change a rule here, change it there too,
// then run the rules check in the notebook to confirm they still match.
//
// Nothing in this file touches the page. Every function takes plain data
// and gives plain data back.


// The three choices you can make for each piece of evidence.
const RULED_OUT = 'Ruled Out';
const UNKNOWN = 'Unknown';
const FOUND = 'Found';
const EVIDENCE_CHOICES = [RULED_OUT, UNKNOWN, FOUND];

// Every possible result for a ghost, from most likely to eliminated.
const CONFIRMED = 'Confirmed';
const TWO_FOUND = 'Two Found';
const ONE_FOUND = 'One Found';
const OPEN = 'Open';
const ELIMINATED = 'Eliminated';


// Return every kind of evidence used by any ghost, in alphabetical order.
function getEvidenceTypes(ghosts) {
    const evidenceTypes = [];
    for (const ghost of ghosts) {
        for (const evidence of ghost.evidence) {
            if (!evidenceTypes.includes(evidence)) {
                evidenceTypes.push(evidence);
            }
        }
    }
    return evidenceTypes.sort();
}


// Return a fresh set of choices with every piece of evidence set to Unknown.
function newSelections(evidenceTypes) {
    const selections = {};
    for (const evidence of evidenceTypes) {
        selections[evidence] = UNKNOWN;
    }
    return selections;
}


// Decide how well a ghost matches the evidence you have marked.
//
// A ghost is eliminated when either of these is true:
//     you ruled out a piece of evidence this ghost always leaves, or
//     you found a piece of evidence this ghost never leaves.
//
// Otherwise the result depends on how many of its three pieces you found.
function ghostStatus(ghost, selections) {
    let foundCount = 0;

    for (const [evidence, choice] of Object.entries(selections)) {
        const ghostHasIt = ghost.evidence.includes(evidence);

        if (choice === RULED_OUT && ghostHasIt) {
            return ELIMINATED;
        }
        if (choice === FOUND && !ghostHasIt) {
            return ELIMINATED;
        }
        if (choice === FOUND && ghostHasIt) {
            foundCount += 1;
        }
    }

    if (foundCount === 3) {
        return CONFIRMED;
    }
    if (foundCount === 2) {
        return TWO_FOUND;
    }
    if (foundCount === 1) {
        return ONE_FOUND;
    }
    return OPEN;
}


// Return the evidence this ghost leaves that you have not marked yet.
// When a ghost has two pieces found, this is the one thing left to look for.
function remainingEvidence(ghost, selections) {
    const remaining = [];
    for (const evidence of ghost.evidence) {
        const choice = selections[evidence] ?? UNKNOWN;
        if (choice === UNKNOWN) {
            remaining.push(evidence);
        }
    }
    return remaining;
}


// Return an object of each ghost's name and its current result.
function summarize(ghosts, selections) {
    const results = {};
    for (const ghost of ghosts) {
        results[ghost.name] = ghostStatus(ghost, selections);
    }
    return results;
}


// Turn a number of seconds into a clock reading such as 0:02:00.
function formatTime(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const twoDigits = (number) => String(number).padStart(2, '0');
    return `${hours}:${twoDigits(minutes)}:${twoDigits(seconds)}`;
}
