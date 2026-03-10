"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export function TransportBar() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTime, setCurrentTime] = useState("0:00");

  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          setIsPlaying(false);
          return 0;
        }
        const next = prev + 0.5;
        const totalSeconds = Math.floor((next / 100) * 210);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        setCurrentTime(`${minutes}:${seconds.toString().padStart(2, "0")}`);
        return next;
      });
    }, 100);
    return () => clearInterval(interval);
  }, [isPlaying]);

  return (
    <div className="fl-panel-raised flex h-16 shrink-0 items-center border-t border-fl-border bg-fl-bg-dark px-4">
      {/* Transport Controls */}
      <div className="flex items-center gap-1">
        {/* Stop */}
        <button
          onClick={() => {
            setIsPlaying(false);
            setProgress(0);
            setCurrentTime("0:00");
          }}
          className="flex h-8 w-8 items-center justify-center rounded transition-colors hover:bg-fl-bg-light"
        >
          <div className="h-3 w-3 rounded-sm bg-fl-text-secondary" />
        </button>

        {/* Play/Pause */}
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="flex h-8 w-8 items-center justify-center rounded transition-colors hover:bg-fl-bg-light"
        >
          {isPlaying ? (
            <div className="flex gap-0.5">
              <div className="h-3.5 w-1 rounded-sm bg-fl-green" />
              <div className="h-3.5 w-1 rounded-sm bg-fl-green" />
            </div>
          ) : (
            <div className="ml-0.5 h-0 w-0 border-y-[7px] border-l-[10px] border-y-transparent border-l-fl-green" />
          )}
        </button>

        {/* Record */}
        <button className="flex h-8 w-8 items-center justify-center rounded transition-colors hover:bg-fl-bg-light">
          <div className="h-3 w-3 rounded-full bg-fl-red/60" />
        </button>
      </div>

      {/* Time Display - LCD style */}
      <div className="fl-panel-inset ml-4 flex items-center gap-3 rounded bg-fl-bg-darkest px-3 py-1.5">
        <span className="font-mono text-sm tabular-nums text-fl-green">
          {currentTime}
        </span>
        <span className="font-mono text-xs text-fl-text-muted">/ 3:30</span>
      </div>

      {/* Song Info + Progress */}
      <div className="mx-6 flex flex-1 flex-col justify-center gap-1">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-fl-text-primary">
              No track selected
            </span>
            <span className="text-xs text-fl-text-muted">—</span>
            <span className="text-xs text-fl-text-secondary">
              Browse to discover
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] text-fl-text-muted">
              BPM
            </span>
            <span className="font-mono text-xs tabular-nums text-fl-orange">
              120
            </span>
          </div>
        </div>

        {/* Progress Bar - FL Studio playlist style */}
        <div className="fl-panel-inset h-1.5 w-full rounded-full bg-fl-bg-darkest">
          <motion.div
            className="h-full rounded-full bg-fl-orange"
            style={{ width: `${progress}%` }}
            transition={{ duration: 0.1 }}
          />
        </div>
      </div>

      {/* Volume - knob style display */}
      <div className="flex items-center gap-2">
        <VuMeter isPlaying={isPlaying} />
        <div className="flex flex-col items-center">
          <span className="font-mono text-[9px] text-fl-text-muted">VOL</span>
          <div className="fl-panel-inset flex h-5 w-10 items-center justify-center rounded bg-fl-bg-darkest">
            <span className="font-mono text-xs tabular-nums text-fl-green">
              78%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function VuMeter({ isPlaying }: { isPlaying: boolean }) {
  return (
    <div className="flex items-end gap-[2px]">
      {[0, 1, 2, 3, 4].map((i) => (
        <div
          key={i}
          className="w-[3px] overflow-hidden rounded-sm"
          style={{ height: "24px" }}
        >
          <motion.div
            className="w-full rounded-sm"
            style={{
              background:
                i < 3
                  ? "var(--fl-green)"
                  : i < 4
                    ? "var(--fl-yellow)"
                    : "var(--fl-red)",
            }}
            animate={
              isPlaying
                ? {
                    height: [
                      "20%",
                      `${60 + Math.random() * 40}%`,
                      `${30 + Math.random() * 50}%`,
                      `${50 + Math.random() * 50}%`,
                      "20%",
                    ],
                  }
                : { height: "10%" }
            }
            transition={
              isPlaying
                ? {
                    duration: 0.4 + i * 0.08,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }
                : { duration: 0.3 }
            }
          />
        </div>
      ))}
    </div>
  );
}
