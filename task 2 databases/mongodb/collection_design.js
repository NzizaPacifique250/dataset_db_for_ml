// ============================================================
// Metro Interstate Traffic Volume - MongoDB Collection Design
// Run this in mongosh: mongosh < collection_design.js
// ============================================================

// Switch to (or create) the database
use("traffic_db");

// Drop existing collection if it exists (for clean re-runs)
db.traffic_data.drop();

// Create the collection with schema validation
db.createCollection("traffic_data", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["date_time", "traffic_volume", "weather"],
      properties: {
        date_time: {
          bsonType: "date",
          description: "Timestamp of the traffic observation - required"
        },
        traffic_volume: {
          bsonType: "int",
          description: "Hourly traffic volume count - required"
        },
        weather: {
          bsonType: "object",
          required: ["main", "description", "temp"],
          properties: {
            main: {
              bsonType: "string",
              description: "Main weather category (e.g., Clouds, Clear, Rain)"
            },
            description: {
              bsonType: "string",
              description: "Detailed weather description"
            },
            temp: {
              bsonType: "number",
              description: "Temperature in Kelvin"
            },
            rain_1h: {
              bsonType: "number",
              description: "Rainfall in the last hour (mm)"
            },
            snow_1h: {
              bsonType: "number",
              description: "Snowfall in the last hour (mm)"
            },
            clouds_all: {
              bsonType: "int",
              description: "Cloud coverage percentage"
            }
          }
        },
        holiday: {
          bsonType: ["string", "null"],
          description: "Holiday name or null if not a holiday"
        }
      }
    }
  }
});

// Create indexes for efficient querying
db.traffic_data.createIndex({ date_time: 1 });
db.traffic_data.createIndex({ "weather.main": 1 });
db.traffic_data.createIndex({ holiday: 1 });

// ============================================================
// Insert sample documents
// ============================================================
db.traffic_data.insertMany([
  {
    date_time: ISODate("2012-10-02T09:00:00Z"),
    traffic_volume: NumberInt(5545),
    weather: {
      main: "Clouds",
      description: "scattered clouds",
      temp: 288.28,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(40)
    },
    holiday: null
  },
  {
    date_time: ISODate("2012-10-02T10:00:00Z"),
    traffic_volume: NumberInt(4516),
    weather: {
      main: "Clouds",
      description: "broken clouds",
      temp: 289.36,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(75)
    },
    holiday: null
  },
  {
    date_time: ISODate("2012-10-02T14:00:00Z"),
    traffic_volume: NumberInt(5181),
    weather: {
      main: "Clear",
      description: "sky is clear",
      temp: 291.72,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(1)
    },
    holiday: null
  },
  {
    date_time: ISODate("2012-12-25T12:00:00Z"),
    traffic_volume: NumberInt(1890),
    weather: {
      main: "Snow",
      description: "light snow",
      temp: 270.15,
      rain_1h: 0.0,
      snow_1h: 0.5,
      clouds_all: NumberInt(90)
    },
    holiday: "Christmas Day"
  },
  {
    date_time: ISODate("2013-07-04T15:00:00Z"),
    traffic_volume: NumberInt(3200),
    weather: {
      main: "Clear",
      description: "sky is clear",
      temp: 301.48,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(5)
    },
    holiday: "Independence Day"
  },
  {
    date_time: ISODate("2013-06-01T08:00:00Z"),
    traffic_volume: NumberInt(4200),
    weather: {
      main: "Rain",
      description: "light rain",
      temp: 290.50,
      rain_1h: 2.5,
      snow_1h: 0.0,
      clouds_all: NumberInt(80)
    },
    holiday: null
  },
  {
    date_time: ISODate("2013-06-01T17:00:00Z"),
    traffic_volume: NumberInt(6100),
    weather: {
      main: "Clouds",
      description: "overcast clouds",
      temp: 295.30,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(95)
    },
    holiday: null
  },
  {
    date_time: ISODate("2014-01-15T07:00:00Z"),
    traffic_volume: NumberInt(5800),
    weather: {
      main: "Mist",
      description: "mist",
      temp: 268.40,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(60)
    },
    holiday: null
  },
  {
    date_time: ISODate("2014-09-01T10:00:00Z"),
    traffic_volume: NumberInt(2500),
    weather: {
      main: "Clear",
      description: "sky is clear",
      temp: 296.00,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(0)
    },
    holiday: "Labor Day"
  },
  {
    date_time: ISODate("2018-09-30T23:00:00Z"),
    traffic_volume: NumberInt(1680),
    weather: {
      main: "Clouds",
      description: "few clouds",
      temp: 282.00,
      rain_1h: 0.0,
      snow_1h: 0.0,
      clouds_all: NumberInt(20)
    },
    holiday: null
  }
]);

// Verify insertion
print("Documents inserted: " + db.traffic_data.countDocuments());
print("\nSample document:");
printjson(db.traffic_data.findOne());
