# Here are all the global variables

# Needed for the authentication
CLIENT_ID = ""
CLIENT_SECRET = ""

DATA_SET = ""

evalscript = """
//VERSION=3
// To set custom max and min values, set
// defaultVis to false and choose your max and
// min values. The color map will then be scaled
// to those max and min values

// LST has two observations per days: 1h30 and 13h30 solar local time

// const defaultVis = true; // true or false
// const color_min = 263; // default min: 263
// const color_max = 340; // default max: 340
const sensing_time = "13"; // "0130" or "1330" or ""

//set the data for map and timeserie
function setup() {
    return {
        input: ["LST", "dataMask"],
        output: [
            //{ id: "default", bands: 4 },
            //{ id: "index", bands: 1, sampleType: "FLOAT32" },
            { id: "LST", bands: 1, sampleType: "FLOAT32" },
            { id: "dataMask", bands: 1 }
        ],
        mosaicking: "TILE"
    };
}

//Select files based on sensing time (0130 or 1330)
function preProcessScenes(collections) {
    collections.scenes.tiles = collections.scenes.tiles.filter(function (tile) {
        return tile.dataPath.includes("T" + sensing_time);
    });
    return collections;
}

function evaluatePixel(samples) {
    // LST scale factor
    const scaleFactor = 100;

    // use the first sample with a datamask of 1
    datamask = 0;
    val = 0/0;
    for (var i = 0; i < samples.length; i++) {
        datamask = samples[i].dataMask;
        if (datamask == 1) {
            val = samples[i].LST / scaleFactor;
            break;
        }
    }    
    
    return {
        //default: [...visualizer.process(val), datamask],
        //index: [val],
        LST: [val, datamask],
        dataMask: [datamask],
    };
}
"""