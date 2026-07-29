import { useCallback, useEffect, useState } from "react";
import ResultPage from "./pages/ResultPage";
import StartPage from "./pages/StartPage";
import SurveyPage from "./pages/SurveyPage";

function normalizePath(pathname: string) {
  if (pathname === "/" || pathname === "/start" || pathname === "/survey") {
    return pathname;
  }
  return "/start";
}

export default function App() {
  const [path, setPath] = useState(() => normalizePath(window.location.pathname));

  useEffect(() => {
    const handlePopState = () => setPath(normalizePath(window.location.pathname));
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const navigate = useCallback((nextPath: string) => {
    window.history.pushState({}, "", nextPath);
    setPath(normalizePath(nextPath));
  }, []);

  const replace = useCallback((nextPath: string) => {
    window.history.replaceState({}, "", nextPath);
    setPath(normalizePath(nextPath));
  }, []);

  if (path === "/survey") {
    return <SurveyPage onReplace={replace} />;
  }

  if (path === "/") {
    return <ResultPage />;
  }

  return <StartPage onNavigate={navigate} />;
}
