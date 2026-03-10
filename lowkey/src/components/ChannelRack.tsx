"use client";

import { motion } from "framer-motion";

interface Track {
  title: string;
  artist: string;
  bpm: number;
  duration: string;
  color: string;
}

const featuredTracks: Track[] = [
  { title: "Midnight Drift", artist: "KVNG", bpm: 140, duration: "3:22", color: "#ff6600" },
  { title: "Neon Shadows", artist: "Synthwave.exe", bpm: 128, duration: "4:15", color: "#4a9eff" },
  { title: "Velvet", artist: "Amara Joy", bpm: 92, duration: "3:45", color: "#ff3333" },
  { title: "2AM Thoughts", artist: "lofi.sage", bpm: 85, duration: "2:58", color: "#7ed321" },
  { title: "Concrete Jungle", artist: "Brick$", bpm: 155, duration: "2:44", color: "#ffd700" },
  { title: "Dissolve", artist: "Echo Park", bpm: 110, duration: "5:02", color: "#00d4aa" },
  { title: "Static Dreams", artist: "NullPtr", bpm: 135, duration: "3:17", color: "#9966ff" },
  { title: "Rust Belt", artist: "Detroitwave", bpm: 145, duration: "3:50", color: "#ff6699" },
];

export function ChannelRack() {
  return (
    <div className="px-8 py-6">
      {/* Section header - FL Studio pattern selector style */}
      <div className="mb-4 flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <div className="h-3 w-3 rounded-sm bg-fl-orange" />
          <h2 className="font-mono text-sm font-bold uppercase tracking-wider text-fl-text-primary">
            Trending Now
          </h2>
        </div>
        <div className="h-px flex-1 bg-fl-border" />
        <div className="flex items-center gap-2">
          {["ALL", "NEW", "HOT"].map((filter) => (
            <button
              key={filter}
              className="rounded border border-fl-border px-2 py-0.5 font-mono text-[10px] text-fl-text-muted transition-colors hover:border-fl-orange hover:text-fl-orange"
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Channel Rack Track List */}
      <div className="fl-panel-inset overflow-hidden rounded border border-fl-border bg-fl-bg-darkest">
        {/* Header Row */}
        <div className="flex items-center border-b border-fl-border bg-fl-bg-dark px-3 py-1.5">
          <span className="w-8 font-mono text-[9px] text-fl-text-muted">#</span>
          <span className="w-8 font-mono text-[9px] text-fl-text-muted" />
          <span className="flex-1 font-mono text-[9px] text-fl-text-muted">
            TRACK
          </span>
          <span className="w-32 font-mono text-[9px] text-fl-text-muted">
            ARTIST
          </span>
          <span className="w-16 text-center font-mono text-[9px] text-fl-text-muted">
            BPM
          </span>
          <span className="w-16 text-right font-mono text-[9px] text-fl-text-muted">
            TIME
          </span>
          <span className="w-24 text-right font-mono text-[9px] text-fl-text-muted">
            LEVEL
          </span>
        </div>

        {/* Track Rows */}
        {featuredTracks.map((track, i) => (
          <motion.div
            key={track.title}
            className="group flex cursor-pointer items-center border-b border-fl-border/50 px-3 py-2 transition-colors last:border-b-0 hover:bg-fl-bg-medium"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            {/* Track number */}
            <span className="w-8 font-mono text-xs tabular-nums text-fl-text-muted">
              {(i + 1).toString().padStart(2, "0")}
            </span>

            {/* Play button / LED */}
            <div className="flex w-8 items-center">
              <div
                className="h-2.5 w-2.5 rounded-full transition-all group-hover:scale-125"
                style={{
                  backgroundColor: track.color,
                  boxShadow: `0 0 4px ${track.color}40`,
                }}
              />
            </div>

            {/* Track name */}
            <div className="flex-1">
              <span className="text-sm text-fl-text-primary transition-colors group-hover:text-fl-orange">
                {track.title}
              </span>
            </div>

            {/* Artist */}
            <span className="w-32 font-mono text-xs text-fl-text-secondary">
              {track.artist}
            </span>

            {/* BPM - LCD style */}
            <div className="flex w-16 justify-center">
              <span className="rounded bg-fl-bg-dark px-1.5 py-0.5 font-mono text-[10px] tabular-nums text-fl-orange">
                {track.bpm}
              </span>
            </div>

            {/* Duration */}
            <span className="w-16 text-right font-mono text-xs tabular-nums text-fl-text-muted">
              {track.duration}
            </span>

            {/* Mini level meter */}
            <div className="flex w-24 items-center justify-end gap-[1px]">
              {Array.from({ length: 16 }).map((_, j) => (
                <div
                  key={j}
                  className="h-3 w-[3px] rounded-[1px]"
                  style={{
                    backgroundColor:
                      j < 10
                        ? j < Math.floor(Math.random() * 6 + 8)
                          ? "var(--fl-green)"
                          : "var(--fl-bg-lighter)"
                        : j < 14
                          ? j < Math.floor(Math.random() * 4 + 10)
                            ? "var(--fl-yellow)"
                            : "var(--fl-bg-lighter)"
                          : "var(--fl-bg-lighter)",
                  }}
                />
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
