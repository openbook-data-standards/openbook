# OpenBook controlled vocabulary — segments

Version `0.3.0-draft`. A **segment** is a slice *inside a match*. Ids are
`segment:<sport>:<slice>`; the formal form is `urn:openbook:segment:<sport>:<slice>`.
Every sport has `full-time` (the whole contest as graded, including any
overtime rules the league's `ruleset` states) and `regulation` where the
distinction matters. Vendors number these differently (Pinnacle period 0 is the
full contest — except in hockey); OpenBook names them.

## Soccer — `segment:soccer:`
`full-time` · `1st-half` · `2nd-half` · `regulation` · `extra-time` · `extra-time-1st-half` · `extra-time-2nd-half` · `penalties`

## Basketball — `segment:basketball:`
`full-time` · `regulation` · `1st-half` · `2nd-half` · `1st-quarter` · `2nd-quarter` · `3rd-quarter` · `4th-quarter` · `overtime`

## American football — `segment:american-football:`
`full-time` · `regulation` · `1st-half` · `2nd-half` · `1st-quarter` · `2nd-quarter` · `3rd-quarter` · `4th-quarter` · `overtime`

## Ice hockey — `segment:ice-hockey:`
`full-time` (OT and shootout included) · `regulation` (60 minutes) · `1st-period` · `2nd-period` · `3rd-period` · `overtime` · `shootout`

## Baseball — `segment:baseball:`
`full-time` · `1st-half` (innings 1–5) · `inning-1` … `inning-9` · `extra-innings` · `first-7-innings`

## Tennis — `segment:tennis:`
`full-time` · `set-1` … `set-5` · `set-<n>-game-<m>` (per-game markets) · `tiebreak-<n>`

## Volleyball / table tennis / badminton — `segment:<sport>:`
`full-time` · `set-1` … `set-7` (volleyball to 5; table tennis to 7; badminton to 3)

## MMA / boxing — `segment:mma:` · `segment:boxing:`
`full-time` · `round-1` … `round-12`

## Golf — `segment:golf:`
`full-time` · `round-1` … `round-4` · `front-9` · `back-9` · `hole-1` … `hole-18`

## Motorsport — `segment:motorsport:`
Qualifying, Sprint and Race are separate **fixtures**; their internal slices:
`full-session` · `q1` · `q2` · `q3` · `lap-<n>` · `first-lap`

## Cricket — `segment:cricket:`
`full-match` · `1st-innings` · `2nd-innings` · `over-<n>` · `powerplay`

## Rugby (union & league) — `segment:rugby-union:` · `segment:rugby-league:`
`full-time` · `1st-half` · `2nd-half` · `regulation` · `extra-time`

## Athletics — `segment:athletics:`
`final` · `heat-<n>` · `semi-final-<n>` · `attempt-<n>` (jumps/throws) · `lap-<n>`

---
Additions go through `CONTRIBUTING.md`; ids are stable once published.
