import { useState, useCallback } from "react";

/**
 * Recruiter search page — plain-language profile search.
 *
 * Designed for Didier: a textarea where the recruiter describes the
 * profile they are looking for in natural language.  Results will be
 * powered by the semantic matching engine (Sprint S3).
 */
function RecruteurPage() {
  const [query, setQuery] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = useCallback(() => {
    if (query.trim().length === 0) return;
    // TODO: call apiPost("/api/matching/search", { query })
    setHasSearched(true);
  }, [query]);

  return (
    <div className="mx-auto flex max-w-lg flex-col gap-6">
      <h2 className="text-2xl font-bold text-slate-800">
        Recherche de profils
      </h2>

      {/* Search input */}
      <label htmlFor="search-query" className="sr-only">
        Décrivez le profil recherché
      </label>
      <textarea
        id="search-query"
        className="min-h-[120px] w-full rounded-lg border border-slate-300 bg-white p-4 text-lg
          text-slate-800 placeholder-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2
          focus:ring-blue-300"
        placeholder="Décrivez le profil recherché..."
        aria-label="Décrivez le profil recherché"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* Search button */}
      <button
        type="button"
        onClick={handleSearch}
        disabled={query.trim().length === 0}
        aria-label="Lancer la recherche"
        className="w-full rounded-lg bg-blue-600 px-6 py-3 text-lg font-semibold text-white
          transition-colors hover:bg-blue-700 focus:outline-none focus-visible:ring-4
          focus-visible:ring-blue-300 disabled:cursor-not-allowed disabled:bg-slate-300"
      >
        Rechercher
      </button>

      {/* Results area */}
      <section
        className="min-h-[160px] rounded-lg border border-slate-200 bg-white p-4"
        aria-label="Résultats de recherche"
        aria-live="polite"
      >
        {hasSearched ? (
          <p className="text-center text-slate-500">
            Aucun résultat pour le moment.
          </p>
        ) : (
          <p className="text-center text-sm italic text-slate-400">
            Les résultats apparaîtront ici après votre recherche.
          </p>
        )}
      </section>
    </div>
  );
}

export default RecruteurPage;
