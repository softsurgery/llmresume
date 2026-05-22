import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { FileText, Sparkles, Loader2, Zap, Shield, Globe } from "lucide-react";

export default function GeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/resume/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || "Generation failed");
      }

      const data = await response.json();
      navigate(`/download/${data.job_id}`);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto flex h-16 items-center px-4">
          <div className="flex items-center gap-2">
            <FileText className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">ResumeAI</span>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Badge variant="secondary" className="gap-1">
              <Sparkles className="h-3 w-3" />
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 pt-16 pb-8 text-center">
        <div className="mx-auto max-w-3xl space-y-4">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            Generate Your Professional{" "}
            <span className="bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              CV in Seconds
            </span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Paste your career details and our AI will generate a beautifully
            formatted CV in multiple formats — PDF, HTML, Markdown, and more.
          </p>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 pb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto">
          <div className="flex items-center gap-3 rounded-lg border p-4">
            <Zap className="h-5 w-5 text-primary shrink-0" />
            <div>
              <p className="text-sm font-medium">Lightning Fast</p>
              <p className="text-xs text-muted-foreground">
                Generated in under a minute
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 rounded-lg border p-4">
            <Shield className="h-5 w-5 text-primary shrink-0" />
            <div>
              <p className="text-sm font-medium">Professional Quality</p>
              <p className="text-xs text-muted-foreground">
                Industry-standard formatting
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 rounded-lg border p-4">
            <Globe className="h-5 w-5 text-primary shrink-0" />
            <div>
              <p className="text-sm font-medium">Multiple Formats</p>
              <p className="text-xs text-muted-foreground">
                PDF, HTML, Markdown, Typst
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Form */}
      <section className="container mx-auto px-4 pb-16">
        <Card className="mx-auto max-w-3xl">
          <CardHeader>
            <CardTitle className="text-2xl">
              Enter Your Career Details
            </CardTitle>
            <CardDescription>
              Paste your name, summary, education, experience, skills, projects,
              languages, and any other relevant information.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder={`Example:\n\nJohn Doe – Software Engineer\nEmail: john@example.com\nLocation: San Francisco, CA\n\nSummary: 5+ years of experience in full-stack development...\n\nExperience:\n- Senior Developer at TechCorp (2021–Present)\n- Developer at StartupXYZ (2019–2021)\n\nEducation:\n- BS Computer Science, Stanford University (2019)\n\nSkills: React, TypeScript, Python, AWS, Docker...`}
                className="min-h-[280px] resize-y font-mono text-sm"
                required
                disabled={loading}
              />

              {error && (
                <div className="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
                  {error}
                </div>
              )}

              <Button
                type="submit"
                size="xl"
                className="w-full"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating your CV...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5" />
                    Generate CV
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground"></div>
      </footer>
    </div>
  );
}
