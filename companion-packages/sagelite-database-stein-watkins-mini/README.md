# sagelite-database-stein-watkins-mini

Stein-Watkins mini database companion package for `sagelite`.

This package contains the `database_stein_watkins_mini` payload from SageMath
10.9, installed as a Python wheel.  `sagelite` depends on this small
redistributable package by default so installed-wheel doctests and
`SteinWatkinsAllData` / `SteinWatkinsPrimeData` lookups can use the mini data
without bundling the full Stein-Watkins database.
