"use client";

import { motion } from "framer-motion";

export function HeroSection() {
  return (
    <div className="relative overflow-hidden border-b border-fl-border bg-fl-bg-dark px-8 py-12">
      {/* Background pattern - piano roll grid */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.03]">
        <div
          className="h-full w-full"
          style={{
            backgroundImage:
              "linear-gradient(var(--fl-border) 1px, transparent 1px), linear-gradient(90deg, var(--fl-border) 1px, transparent 1px)",
            backgroundSize: "40px 20px",
          }}
        />
      </div>

      <div className="relative z-10 mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* DAW-style header with LED indicators */}
          <div className="mb-2 flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-fl-green" style={{ boxShadow: "0 0 6px var(--fl-green)" }} />
            <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-fl-green">
              Now Online
            </span>
          </div>

          <h1 className="mb-4 text-5xl font-bold tracking-tight">
            <span className="text-fl-text-primary">Music Belongs to the </span>
            <span className="text-fl-orange" style={{ textShadow: "0 0 30px rgba(255, 102, 0, 0.3)" }}>
              Underground
            </span>
          </h1>

          <p className="mb-6 max-w-xl text-lg leading-relaxed text-fl-text-secondary">
            Discover artists before the world does. On Lowkey, once an artist hits{" "}
            <span className="font-mono text-fl-yellow">100K</span> monthly listeners,
            they graduate to the{" "}
            <span className="text-fl-yellow">Hall of Fame</span> — making room
            for the next wave.
          </p>

          <div className="flex items-center gap-4">
            <motion.button
              className="fl-panel-raised rounded bg-fl-orange px-6 py-2.5 font-mono text-sm font-bold text-black transition-colors hover:bg-fl-orange-bright"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              START DISCOVERING
            </motion.button>
            <motion.button
              className="rounded border border-fl-border px-6 py-2.5 font-mono text-sm text-fl-text-secondary transition-colors hover:border-fl-orange hover:text-fl-orange"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              I&apos;M AN ARTIST
            </motion.button>
          </div>
        </motion.div>

        {/* Stats bar - LCD display style */}
        <motion.div
          className="fl-panel-inset mt-10 flex items-center justify-between rounded bg-fl-bg-darkest px-6 py-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <StatBlock label="ACTIVE ARTISTS" value="12,847" color="var(--fl-orange)" />
          <Divider />
          <StatBlock label="TRACKS" value="84,291" color="var(--fl-green)" />
          <Divider />
          <StatBlock label="HALL OF FAME" value="342" color="var(--fl-yellow)" />
          <Divider />
          <StatBlock label="LISTENERS TODAY" value="1.2M" color="var(--fl-blue)" />
        </motion.div>
      </div>
    </div>
  );
}

function StatBlock({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div className="flex flex-col items-center gap-1">
      <span className="font-mono text-[9px] tracking-widest text-fl-text-muted">
        {label}
      </span>
      <span
        className="font-mono text-xl font-bold tabular-nums"
        style={{ color }}
      >
        {value}
      </span>
    </div>
  );
}

function Divider() {
  return <div className="h-8 w-px bg-fl-border" />;
}
