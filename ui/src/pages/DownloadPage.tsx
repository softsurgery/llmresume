import { useEffect, useState } from "react"
import { useParams, Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  FileText,
  Download,
  CheckCircle2,
  ArrowLeft,
  FileCode,
  FileType,
  File,
  Loader2,
} from "lucide-react"

interface FileInfo {
  name: string
  ext: string
  ext_upper: string
  url: string
}

const extIconMap: Record<string, React.ReactNode> = {
  pdf: <FileText className="h-6 w-6 text-red-500" />,
  html: <FileCode className="h-6 w-6 text-blue-500" />,
  md: <FileType className="h-6 w-6 text-purple-500" />,
  yaml: <File className="h-6 w-6 text-pink-500" />,
  tex: <File className="h-6 w-6 text-yellow-600" />,
  png: <File className="h-6 w-6 text-green-500" />,
}

const extColorMap: Record<string, string> = {
  pdf: "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800",
  html: "bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-800",
  md: "bg-purple-50 border-purple-200 dark:bg-purple-950 dark:border-purple-800",
  yaml: "bg-pink-50 border-pink-200 dark:bg-pink-950 dark:border-pink-800",
  tex: "bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-800",
  png: "bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800",
}

export default function DownloadPage() {
  const { jobId } = useParams<{ jobId: string }>()
  const [files, setFiles] = useState<FileInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await fetch(`/api/resume/${jobId}/files/`)
        if (!response.ok) {
          throw new Error("Failed to load files")
        }
        const data = await response.json()
        setFiles(data.files)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load files")
      } finally {
        setLoading(false)
      }
    }

    fetchFiles()
  }, [jobId])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary" />
          <p className="text-muted-foreground">Loading your files...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto flex h-16 items-center px-4">
          <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <FileText className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">ResumeAI</span>
          </Link>
        </div>
      </header>

      {/* Content */}
      <section className="container mx-auto px-4 py-12">
        <div className="mx-auto max-w-3xl space-y-8">
          {/* Success Banner */}
          <div className="text-center space-y-4">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 dark:bg-green-900">
              <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Your CV is Ready!
            </h1>
            <p className="text-muted-foreground text-lg">
              Download your professionally formatted CV in your preferred format.
            </p>
            <Badge variant="secondary" className="gap-1">
              <CheckCircle2 className="h-3 w-3" />
              Generated successfully
            </Badge>
          </div>

          {/* Error State */}
          {error && (
            <div className="rounded-md bg-destructive/10 border border-destructive/20 p-4 text-center text-destructive">
              {error}
            </div>
          )}

          {/* Download Cards */}
          {files.length > 0 ? (
            <Card>
              <CardHeader>
                <CardTitle>Download Formats</CardTitle>
                <CardDescription>
                  Choose the format that works best for you
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {files.map((file) => (
                    <a
                      key={file.name}
                      href={file.url}
                      download
                      className={`group flex items-center gap-4 rounded-lg border p-4 transition-all hover:shadow-md hover:-translate-y-0.5 ${extColorMap[file.ext] || "bg-muted"}`}
                    >
                      <div className="shrink-0">
                        {extIconMap[file.ext] || <File className="h-6 w-6 text-muted-foreground" />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{file.name}</p>
                        <p className="text-xs text-muted-foreground">{file.ext_upper} Format</p>
                      </div>
                      <Download className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                    </a>
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
            !error && (
              <Card>
                <CardContent className="py-8 text-center text-muted-foreground">
                  No files were generated. Please try again.
                </CardContent>
              </Card>
            )
          )}

          {/* Back Button */}
          <div className="text-center">
            <Button variant="outline" size="lg" asChild>
              <Link to="/">
                <ArrowLeft className="h-4 w-4" />
                Generate Another CV
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
