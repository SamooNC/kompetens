/**
 * Helper (Aidant) page — companion mode for Nadia.
 *
 * In this mode a librarian, social worker, or community helper sits
 * next to the job-seeker and guides them through the vocal inventory.
 * The helper sees instructions and controls on their screen while the
 * candidate interacts via voice.
 *
 * Currently a scaffold — the full dual-screen flow is planned for
 * Sprint S4.
 */
function AidantPage() {
  return (
    <div className="mx-auto flex max-w-lg flex-col gap-6">
      <h2 className="text-2xl font-bold text-slate-800">Mode Aidant</h2>
      <p className="text-lg text-slate-600">
        Accompagnez un candidat dans son inventaire de compétences.
      </p>

      {/* Instructions */}
      <div className="rounded-lg border border-slate-200 bg-white p-5">
        <h3 className="mb-3 text-lg font-semibold text-slate-700">
          Comment ça marche ?
        </h3>
        <ol className="list-inside list-decimal space-y-2 text-slate-600">
          <li>Installez-vous à côté du candidat.</li>
          <li>Lancez l'accompagnement ci-dessous.</li>
          <li>
            Guidez le candidat : vous voyez les questions, il répond à voix
            haute.
          </li>
          <li>Validez chaque étape ensemble avant de passer à la suivante.</li>
        </ol>
      </div>

      {/* Start button */}
      <button
        type="button"
        aria-label="Commencer un accompagnement"
        className="w-full rounded-lg bg-blue-600 px-6 py-4 text-lg font-semibold text-white
          transition-colors hover:bg-blue-700 focus:outline-none focus-visible:ring-4
          focus-visible:ring-blue-300"
      >
        Commencer un accompagnement
      </button>
    </div>
  );
}

export default AidantPage;
