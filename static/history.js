// the start date of our histoy bar
minTime = 2016;
// the end date of our histoy bar
maxTime = 2018;
// defines the era; either CE or BCE
era = " CE";

// the amount by which we need to jump
deltaTime = maxTime - minTime;
// the width of the bar
barWidth = screen.width * 0.95;

// only use maximum of 10 cursor labels
cursorCount = Math.min((maxTime - minTime - 1), 10);
const MAX_CURSOR_COUNT = 10;
// store the cursors for a maximum of 10 cursors
cursors = new Array(MAX_CURSOR_COUNT);

const MAX_DATA_POINT_COUNT = 20;
// store the cursors for showing data values
data_cursors = new Array(MAX_DATA_POINT_COUNT);

spawnCursors();
getData();

/******************************
 * methods for managing time
******************************/
function setTime() {
    // document.getElementById("start").innerHTML = Math.abs(minTime) + era;
    // document.getElementById("end").innerHTML   = Math.abs(maxTime) + era;
    start = document.getElementById("start");
    end   = document.getElementById("end");

    readableStartDate = getReadableNumber(Math.abs(minTime));
    readableEndDate   = getReadableNumber(Math.abs(maxTime));

    start.innerHTML   = readableStartDate + era;
    end.innerHTML     = readableEndDate + era;

    start.style.width = getArrowLabelWidth(readableStartDate) + "px";
    end.style.width   = getArrowLabelWidth(readableEndDate) + "px";
    updateCursorCount();
    updateEra();
}

function updateEra() {
    era = (minTime > 0) ? " CE" : " BCE";
}

function decreaseTime() {
    minTime -= deltaTime;
    maxTime -= deltaTime;
    setTime();
    getData();
}

function increaseTime() {
    minTime += deltaTime;
    maxTime += deltaTime;
    setTime();
    getData();
}

function increaseTimeDelta() {
    // increase the range of years whenever range is increased
    minTime -= deltaTime / 2;
    maxTime += deltaTime / 2;
    // increase in increments of 'times 2'
    deltaTime *= 2;
    setTime();
    getData();
}

function decreaseTimeDelta() {
    if (deltaTime <= 2) {
        return;
    }
    // only decrease deltaTime later to avoid race condition
    deltaTime /= 2;
    // decrease the range of years whenever range is decreased
    minTime += deltaTime / 2;
    maxTime -= deltaTime / 2;
    setTime();
    getData();    
}

/*******************************************
*  methods for managing cursors
*******************************************/

function updateCursorCount() {
    cursorCount = Math.min((maxTime - minTime - 1), 10);
    // removeExcessiveCursors(cursors, cursorCount);
    spawnCursors();
}

// returns the number of non-null values in cursors
function getCursorsCount(cursors) {
    count = 0;
    for (i = 0; i < cursors.length; ++i)
        if ((cursors[i] != 0) && (cursors[i] != null)) 
            ++count;
    return count;
}

// returns the offset of targetDate with respect to date in the bar
function getCursorOffset(targetDate) {
    return (targetDate - minTime) / (maxTime - minTime)
}

// returns the left indent for the arrows
function getLeftIndent(targetDate) {
    return getCursorOffset(targetDate) * barWidth + 0.015 * screen.width + "px";
    // return getCursorOffset(dates[i]) * barWidth +  "px";
}

function reverseString(str) {
    return str.split("").reverse().join("");
}

function getReadableNumber(targetDate) {
    strTargetDate = String(targetDate);
    reverseDate = reverseString(strTargetDate);
    readableDate = "";
    for (i = 0; i < strTargetDate.length; i++) {
        readableDate += reverseDate[i];
        // the ',' comes after every 3 digits; e.g> 2,048,576
        if (((i + 1) % 3 == 0) && (i+1 != strTargetDate.length))
            readableDate += ",";
    }
    return reverseString(readableDate);
}

// returns the width to be used for the arrow label
function getArrowLabelWidth(targetDate) {
    // reserver 8 pixels per character in targetDate
    return Math.max(8*targetDate.length, 50);
}

// set the cursor to the targetDate and corresponding offset in the bar
function setCursor(cursor, targetDate) {
    if (targetDate > maxTime || targetDate < minTime)
        return;

    // cursor.style.left = getCursorOffset(targetDate) * barWidth + "px";
    cursor.style.left = getLeftIndent(targetDate);

    // the label is the first and only child of cursor
    label = cursor.firstElementChild;

    if (targetDate > -1000 && targetDate < 1000) {
        era = (targetDate > 0) ? "<br>CE" : "<br>BCE";
    } else {
        era = (targetDate > 0) ? " CE" : " BCE";
    }

    // label.innerHTML = Math.abs(targetDate) + era;
    targetDate = Math.abs(targetDate);
    readableDate = getReadableNumber(targetDate);

    label.innerHTML = readableDate + era;
    label.style.width = getArrowLabelWidth(readableDate) + "px";
}

// create a cursor DOM Element and return it after setting it to targetDate
function createCursor(id, leftIndent, targetDate) {
    var cursor = document.createElement("div");
    cursor.classList = "cursor start-cursor";
    cursor.id = "cursor" + id;
    cursor.style.left = leftIndent;

    var label = document.createElement("div");
    label.classList = "arrow-label card-title";
    
    era = (targetDate > 0) ? " CE" : " BCE";
    targetDate = Math.abs(targetDate);
    readableDate = getReadableNumber(targetDate);

    label.innerHTML = readableDate + era;
    label.style.width = getArrowLabelWidth(readableDate) + "px";

    cursor.appendChild(label);
    return cursor;
}

// returns the date where cursors should be spawned
function getCursorDates() {
    dates = Array();
    for (i = 1; i < cursorCount+1; ++i) {
        // add 1 to cursourCount since n cursors divide bar in (n+1) regions
        tempDate = minTime + (i /(cursorCount + 1)) * (maxTime - minTime);
        dates.push(Math.floor(tempDate));
    }
    return dates;
}

// spawns the required number of cursors
function spawnCursors() {
    dates = getCursorDates();
    var i = 0;
    for (; i < cursorCount; ++i) {
        // evenly space cursors
        leftIndent = getLeftIndent(dates[i]);

        if (cursors[i] == null) {
            cursor = createCursor(i, leftIndent, dates[i]);
            document.body.appendChild(cursor);
            cursors[i] = cursor;
        } else {
            // reuse cursor already spawned
            setCursor(cursors[i], dates[i]);
        }
        // set it to dislay in case it was hidden before
        cursors[i].style.display = "block";
    }
    // all other cursors are currently not in use, so hide them
    for (; i < cursors.length; ++i) {
        if (cursors[i] != null)
            cursors[i].style.display = "none";
    }
}

/*************************************
 * methods for handling data
*************************************/

// returns string with underscore replaced with space
function removeUnderscore(string) {
    return string.replace(/_/g, ' ');
}

// gets the data from the server using GET request
function getData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            setData(this.responseText);
        }
    };
    randomize  = document.getElementById("randomize").checked;
    load_count = document.getElementById("load_count").value;
    xhttp.open("GET", "/history_data?start=" + minTime + "&end=" + maxTime + "&random=" + randomize + "&load_count=" + load_count);
    xhttp.send();
}

// returns a cursor DOM Element with date and data set
function createCursorWithData(id, leftIndent, targetDate, data) {
    var cursor = document.createElement("div");
    cursor.classList = "cursor start-cursor";
    cursor.onmouseover = function () { cursor.style.zIndex =  1; };
    cursor.onmouseout  = function () { cursor.style.zIndex = -1; };
    cursor.id = "cursor" + id;
    cursor.style.left = leftIndent;

    var label = document.createElement("div");
    label.classList = "arrow-label card-title";    
    
    era = (targetDate > 0) ? " CE" : " BCE";

    // label.innerHTML = Math.abs(targetDate) + era;
    targetDate = Math.abs(targetDate);
    readableDate = getReadableNumber(targetDate);

    label.innerHTML = readableDate + era;
    label.style.width = getArrowLabelWidth(readableDate) + "px";
    
    cursor.appendChild(label);

    var data_label = document.createElement("div");
    data_label.classList = "data-label card-text";
    data_label.innerHTML = data;
    cursor.appendChild(data_label)

    return cursor;
}

// sets data to the data-label part of cursor
function setDataToCursor(cursor, data) {
    data_label = cursor.lastChild;
    data_label.innerHTML = data;   
}

// check if data contains 'x' or not
function contains(data, x) {
    for (i in data) {
        if (x == data[i]) return true;
    }
    return false;
}

function spawnCursorsWithDataValues(dates, date_values) {
    var i = 0;
    for (; i < dates.length; ++i) {
        if (data_cursors[i] == null) {
            leftIndent = getLeftIndent(dates[i]);
            // set cursor id to 10*i since 'i' was used already
            cursor = createCursorWithData(10*(i+1), leftIndent, dates[i], date_values[i]);
            cursor.style.top = "30%";

            document.body.appendChild(cursor);
            data_cursors[i] = cursor;
        } else {
            setCursor(data_cursors[i], dates[i]);
            setDataToCursor(data_cursors[i], date_values[i]);
            data_cursors[i].style.display = "block";
        }
    }
    // set remaining cursors to hidden if they have been used before
    for (; i < data_cursors.length; ++i) {
        if (data_cursors[i] != null) {
            data_cursors[i].style.display = "none";
        }
    }
}

// sets the data to the center card and also to various data cursors
function setData(data) {
    parsedData = JSON.parse(data);
    // store years and it's corresponsing value for that year
    years = []
    year_values = []
    // store all the content to be displayed as a whole
    s = "";

    for (i in parsedData.values) {
        currentValue = parsedData.values[i];

        cleanTitle = removeUnderscore(currentValue.title);

        if (!contains(years, currentValue.year)) {
            years.push(currentValue.year);
            year_values.push(cleanTitle + ", ");
        } else {
            index = 0;
            // find the index of the year 
            for (; index < years.length; ++index)
                if (years[index] == currentValue.year) break;

            
            if (year_values[index] == null) {
                year_values[index] = cleanTitle + ", ";
            } else {
                // only append the string if it wasn't added already
                if (year_values[index].search(cleanTitle) != -1) continue;
                year_values[index] += cleanTitle + ", ";
            }
        }

        s += "<p class='card-title'>Title: <a href='" + currentValue.link + "'>"  + cleanTitle + "</a></p>";
        s += "<p class='card-text'>Year:" + currentValue.year + "</p>";
        s += "<p class='card-text'>Content: " + currentValue.content + ".</p>";
    }
    // s += "<p>" + years + "</p>"
    // s += "<p>" + year_values + "</p>"

    spawnCursorsWithDataValues(years, year_values);

    document.getElementById("data").innerHTML = s;
}
