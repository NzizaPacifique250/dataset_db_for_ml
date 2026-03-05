// ============================================================
// Metro Interstate Traffic Volume - MongoDB Queries
// Run this in mongosh: mongosh < queries.js
// ============================================================

use("traffic_db");

// ============================================================
// Query 1: Average traffic volume by weather condition
// Uses aggregation pipeline to group by weather type
// ============================================================
print("=== Query 1: Average Traffic Volume by Weather Condition ===");
printjson(
  db.traffic_data.aggregate([
    {
      $group: {
        _id: "$weather.main",
        avg_traffic: { $avg: "$traffic_volume" },
        record_count: { $sum: 1 }
      }
    },
    {
      $project: {
        _id: 0,
        weather_main: "$_id",
        avg_traffic: { $round: ["$avg_traffic", 0] },
        record_count: 1
      }
    },
    { $sort: { avg_traffic: -1 } }
  ]).toArray()
);

// ============================================================
// Query 2: Traffic records within a specific date range
// Filters records between two dates and returns details
// ============================================================
print("\n=== Query 2: Traffic Records for June 1, 2013 ===");
printjson(
  db.traffic_data.find(
    {
      date_time: {
        $gte: ISODate("2013-06-01T00:00:00Z"),
        $lte: ISODate("2013-06-01T23:59:59Z")
      }
    },
    {
      _id: 0,
      date_time: 1,
      traffic_volume: 1,
      "weather.main": 1,
      "weather.description": 1,
      holiday: 1
    }
  ).sort({ date_time: 1 }).toArray()
);

// ============================================================
// Query 3: Compare average traffic on holidays vs non-holidays
// Uses conditional grouping in aggregation
// ============================================================
print("\n=== Query 3: Holiday vs Non-Holiday Traffic ===");
printjson(
  db.traffic_data.aggregate([
    {
      $group: {
        _id: {
          $cond: {
            if: { $ne: ["$holiday", null] },
            then: "Holiday",
            else: "Non-Holiday"
          }
        },
        avg_traffic: { $avg: "$traffic_volume" },
        min_traffic: { $min: "$traffic_volume" },
        max_traffic: { $max: "$traffic_volume" },
        record_count: { $sum: 1 }
      }
    },
    {
      $project: {
        _id: 0,
        day_type: "$_id",
        avg_traffic: { $round: ["$avg_traffic", 0] },
        min_traffic: 1,
        max_traffic: 1,
        record_count: 1
      }
    }
  ]).toArray()
);

// ============================================================
// Query 4: Get the latest (most recent) traffic record
// Sorts by date descending and returns the first document
// ============================================================
print("\n=== Query 4: Latest Traffic Record ===");
printjson(
  db.traffic_data.find(
    {},
    { _id: 0 }
  ).sort({ date_time: -1 }).limit(1).toArray()
);
