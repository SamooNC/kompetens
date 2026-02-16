import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import ConnectionStatus from "./ConnectionStatus";

interface LayoutProps {
  children: ReactNode;
}

/**
 * Application shell: sticky header, scrollable main content,
 * and a bottom navigation bar sized for large touch targets.
 *
 * The bottom nav uses `pb-[env(safe-area-inset-bottom)]` so it
 * clears the home-bar on notched iPhones / Android gesture nav.
 */
function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-[100dvh] flex-col">
      {/* -------- Header -------- */}
      <header className="sticky top-0 z-30 flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 shadow-sm">
        <h1 className="text-lg font-bold text-blue-800">Kompetens</h1>
        <ConnectionStatus />
      </header>

      {/* -------- Main content -------- */}
      <main className="flex-1 overflow-y-auto px-4 py-6">{children}</main>

      {/* -------- Bottom navigation -------- */}
      <nav
        className="sticky bottom-0 z-30 grid grid-cols-4 border-t border-slate-200 bg-white shadow-inner"
        style={{ paddingBottom: "env(safe-area-inset-bottom, 0px)" }}
        aria-label="Navigation principale"
      >
        <NavItem to="/" label="Accueil" icon={<HomeIcon />} />
        <NavItem to="/inventaire" label="Inventaire" icon={<MicIcon />} />
        <NavItem to="/recruteur" label="Recherche" icon={<SearchIcon />} />
        <NavItem to="/aidant" label="Aide" icon={<UsersIcon />} />
      </nav>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Nav helpers                                                       */
/* ------------------------------------------------------------------ */

interface NavItemProps {
  to: string;
  label: string;
  icon: ReactNode;
}

function NavItem({ to, label, icon }: NavItemProps) {
  return (
    <NavLink
      to={to}
      end={to === "/"}
      aria-label={label}
      className={({ isActive }) =>
        `flex flex-col items-center justify-center gap-0.5 py-2 text-xs transition-colors ${
          isActive
            ? "text-blue-700 font-semibold"
            : "text-slate-500 hover:text-slate-700"
        }`
      }
    >
      {icon}
      <span>{label}</span>
    </NavLink>
  );
}

/* ------------------------------------------------------------------ */
/*  Inline SVG icons — no external icon library needed                 */
/* ------------------------------------------------------------------ */

function HomeIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M3 12l2-2m0 0l7-7 7 7m-9-5v12a2 2 0 002 2h4a2 2 0 002-2V7"
      />
    </svg>
  );
}

function MicIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 1a4 4 0 00-4 4v6a4 4 0 008 0V5a4 4 0 00-4-4z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19 11a7 7 0 01-14 0"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 18v4m-3 0h6"
      />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z"
      />
    </svg>
  );
}

function UsersIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M17 20c0-2.21-2.69-4-6-4s-6 1.79-6 4"
      />
      <circle cx="11" cy="8" r="4" />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M21 20c0-1.66-1.34-3-3-3-.86 0-1.63.37-2.17.95"
      />
      <circle cx="18" cy="10" r="3" />
    </svg>
  );
}

export default Layout;
