"use client";

import { motion } from "framer-motion";

interface ArtistCardProps {
  name: string;
  genre: string;
  listeners: number;
  color: string;
  index: number;
}

export function ArtistCard({
  name,
  genre,
  listeners,
  color,
  index,
}: ArtistCardProps) {
  const listenerPercent = Math.min((listeners / 100000) * 100, 100);
  const isNearGraduation = listenerPercent > 80;

  return (
    <motion.div
      className="fl-panel-raised group relative overflow-hidden rounded border border-fl-border bg-fl-bg-dark transition-colors hover:border-fl-border-light"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      whileHover={{ scale: 1.02 }}
    >
      {/* Album art placeholder - mixer channel style */}
      <div
        className="relative flex h-40 items-end justify-center overflow-hidden"
        style={{ background: `linear-gradient(135deg, ${color}20, ${color}05)` }}
      >
        {/* VU Meter bars in background */}
        <div className="absolute inset-0 flex items-end justify-center gap-1 px-6 pb-2 opacity-30 transition-opacity group-hover:opacity-60">
          {Array.from({ length: 12 }).map((_, i) => (
            <motion.div
              key={i}
              className="w-2 rounded-t"
              style={{ backgroundColor: color }}
              animate={{
                height: [
                  `${20 + Math.random() * 30}%`,
                  `${40 + Math.random() * 50}%`,
                  `${20 + Math.random() * 30}%`,
                ],
              }}
              transition={{
                duration: 0.8 + Math.random() * 0.5,
                repeat: Infinity,
                delay: i * 0.1,
                ease: "easeInOut",
              }}
            />
          ))}
        </div>

        {/* Artist initial */}
        <div
          className="relative z-10 mb-4 flex h-16 w-16 items-center justify-center rounded-full border-2"
          style={{
            borderColor: color,
            backgroundColor: `${color}15`,
          }}
        >
          <span
            className="text-2xl font-bold"
            style={{ color }}
          >
            {name[0]}
          </span>
        </div>
      </div>

      {/* Info section - mixer channel label style */}
      <div className="p-3">
        <div className="mb-1 flex items-center justify-between">
          <h3 className="truncate text-sm font-medium text-fl-text-primary">
            {name}
          </h3>
          <div
            className="h-2 w-2 rounded-full"
            style={{
              backgroundColor: color,
              boxShadow: `0 0 4px ${color}60`,
            }}
          />
        </div>
        <p className="font-mono text-[10px] uppercase tracking-wider text-fl-text-muted">
          {genre}
        </p>

        {/* Listener meter - styled like a channel fader */}
        <div className="mt-3">
          <div className="mb-1 flex items-center justify-between">
            <span className="font-mono text-[10px] text-fl-text-muted">
              LISTENERS
            </span>
            <span
              className={`font-mono text-xs tabular-nums ${
                isNearGraduation ? "text-fl-yellow" : "text-fl-text-secondary"
              }`}
            >
              {listeners.toLocaleString()}
            </span>
          </div>
          <div className="fl-panel-inset h-1.5 w-full rounded-full bg-fl-bg-darkest">
            <motion.div
              className="h-full rounded-full"
              style={{
                backgroundColor: isNearGraduation
                  ? "var(--fl-yellow)"
                  : color,
              }}
              initial={{ width: 0 }}
              animate={{ width: `${listenerPercent}%` }}
              transition={{ duration: 0.8, delay: index * 0.05 }}
            />
          </div>
          <div className="mt-1 flex justify-between font-mono text-[9px] text-fl-text-muted">
            <span>0</span>
            <span>100K → HALL OF FAME</span>
          </div>
        </div>
      </div>

      {/* Graduation warning */}
      {isNearGraduation && (
        <motion.div
          className="absolute right-2 top-2 rounded bg-fl-yellow/20 px-2 py-0.5"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <span className="font-mono text-[9px] font-bold text-fl-yellow">
            GRADUATING SOON
          </span>
        </motion.div>
      )}
    </motion.div>
  );
}
