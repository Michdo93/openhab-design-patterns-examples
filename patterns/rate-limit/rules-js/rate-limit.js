const lastAction = cache.private.get("LastAction", () => time.ZonedDateTime.now().minusDays(1));

if (lastAction.isBefore(time.ZonedDateTime.now().minusHours(24))) {
  console.log("Rate-limited action");
  cache.private.put("LastAction", time.ZonedDateTime.now());
}
