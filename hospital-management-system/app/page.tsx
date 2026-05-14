export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">Hospital Management System</h1>
          <p className="text-lg text-muted-foreground mb-8">Desktop Application for Healthcare Organizations</p>
          <div className="bg-card border rounded-lg p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Project Components</h2>
            <div className="grid gap-4 text-left">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary rounded-full"></div>
                <span>Python Desktop Application (Tkinter GUI)</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary rounded-full"></div>
                <span>SQL Database Schema & Sample Data</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary rounded-full"></div>
                <span>Complete Documentation with Screenshots</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary rounded-full"></div>
                <span>Database Backup & Restore Utilities</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
