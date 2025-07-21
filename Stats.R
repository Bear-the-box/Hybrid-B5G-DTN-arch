library(ggplot2)
library(reshape2)

df <- data.frame(
  Interval = factor(c("3600s", "7200s", "14400s"), levels = c("3600s", "7200s", "14400s")),
  Epidemic_DeliveryProb = c(0.72, 0.88, 1.0),
  FL_DeliveryProb = c(0.61, 0.78, 0.92),
  Epidemic_LatencyAvg = c(68.66, 56.63, 49.23),
  FL_LatencyAvg = c(71.04, 59.70, 44.76),
  Epidemic_Overhead = c(17.1, 11.45, 9.64),
  FL_Overhead = c(4.33, 3.97, 3.77),
  Epidemic_HopsAvg = c(2.1, 2.3, 2.5),
  FL_HopsAvg = c(1.9, 2.11, 2.39)
)

library(reshape2)

dp <- melt(df[, c("Interval", "Epidemic_DeliveryProb", "FL_DeliveryProb")], id.vars = "Interval")
ggplot(dp, aes(x = Interval, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Delivery Probability", y = "Probability (%)", x = "Message Interval") +
  theme_minimal()

lat <- melt(df[, c("Interval", "Epidemic_LatencyAvg", "FL_LatencyAvg")], id.vars = "Interval")
ggplot(lat, aes(x = Interval, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Latency Average", y = "Seconds (s)", x = "Message Interval") +
  theme_minimal()

ov <- melt(df[, c("Interval", "Epidemic_Overhead", "FL_Overhead")], id.vars = "Interval")
ggplot(ov, aes(x = Interval, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Overhead Ratio", y = "Overhead", x = "Message Interval") +
  theme_minimal()

hop <- melt(df[, c("Interval", "Epidemic_HopsAvg", "FL_HopsAvg")], id.vars = "Interval")
ggplot(hop, aes(x = Interval, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Average Hop Count", y = "Hops", x = "Message Interval") +
  theme_minimal()

