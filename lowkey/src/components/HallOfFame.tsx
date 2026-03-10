"use client";

import { motion } from "framer-motion";

const graduates = [
  { name: "Midnight Collective", genre: "Electronic", peakListeners: "142K", graduatedDate: "Feb 2026", color: "#ffd700" },
  { name: "Sarah Waves", genre: "R&B", peakListeners: "118K", graduatedDate: "Jan 2026", color: "#ffd700" },
  { name: "BLVCK COFFEE", genre: "Hip Hop", peakListeners: "203K", graduatedDate: "Jan 2026", color: "#ffd700" },
  { name: "Pixel Dreams", genre: "Lo-Fi", peakListeners: "105K", graduatedDate: "Dec 2025", color: "#ffd700" },
  { name: "The Basement Tapes", genre: "Indie Rock", peakListeners: "131K", graduatedDate: "Dec 2025", color: "#ffd700" },
];

export function HallOfFame() {
  return (
    <div className="border-t border-fl-border px-8 py-8">
      <div className="mb-6 flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <motion.div
            className="h-3 w-3 rounded-sm bg-fl-yellow"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
          <h2 className="font-mono text-sm font-bold uppercase tracking-wider text-fl-yellow">
            Hall of Fame
          </h2>
        </div>
        <div className="h-px flex-1 bg-fl-border" />
        <span className="font-mono text-[10px] text-fl-text-muted">
          GRADUATED ARTISTS — 100K+ LISTENERS
        </span>
      </div>

      <div className="fl-panel-inset overflow-hidden rounded border border-fl-yellow/20 bg-fl-bg-darkest">
        {graduates.map((grad, i) => (
          <motion.div
            key={grad.name}
            className="group flex items-center border-b border-fl-border/30 px-4 py-3 last:border-b-0"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: i * 0.1 }}
          >
            {/* Trophy / rank */}
            <div className="flex w-10 items-center">
              <span className="font-mono text-lg text-fl-yellow">
                {i === 0 ? "♛" : "★"}
              </span>
            </div>

            {/* Artist info */}
            <div className="flex-1">
              <span className="text-sm font-medium text-fl-yellow/90">
                {grad.name}
              </span>
              <span className="ml-2 font-mono text-[10px] uppercase text-fl-text-muted">
                {grad.genre}
              </span>
            </div>

            {/* Peak listeners */}
            <div className="flex items-center gap-1">
              <span className="font-mono text-[9px] text-fl-text-muted">
                PEAK
              </span>
              <span className="font-mono text-sm tabular-nums text-fl-yellow">
                {grad.peakListeners}
              </span>
            </div>

            {/* Graduation date */}
            <div className="ml-6 flex items-center gap-1">
              <span className="font-mono text-[9px] text-fl-text-muted">
                GRADUATED
              </span>
              <span className="font-mono text-xs text-fl-text-secondary">
                {grad.graduatedDate}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Footer message */}
      <div className="mt-4 text-center">
        <p className="font-mono text-xs text-fl-text-muted">
          When an artist surpasses 100,000 monthly listeners, they graduate from
          Lowkey and enter the Hall of Fame — making space for the next wave of
          underground talent.
        </p>
      </div>
    </div>
  );
}
