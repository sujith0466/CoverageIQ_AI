import axios from 'axios';

export interface UploadResponse {
  success: boolean;
  report_id?: string;
  filename?: string;
  status?: string;
  message?: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FileCoverage {
  filename: string;
  lines_valid: number;
  lines_covered: number;
  coverage_percent: number;
}

export interface AnalyzeResponse {
  success: boolean;
  coverage_percent?: number;
  total_files?: number;
  total_classes?: number;
  total_lines?: number;
  covered_lines?: number;
  line_rate?: number;
  branch_rate?: number;
  files?: FileCoverage[];
  message?: string;
}

export interface FunctionData {
  name: string;
  file_path: string;
  start_line?: number;
  end_line?: number;
  function_type?: string;
  is_async?: boolean;
}

export interface ScanResponse {
  success: boolean;
  total_functions_found?: number;
  functions?: FunctionData[];
  message?: string;
}

export interface GapFunctionData {
  id?: string;
  name: string;
  file_path: string;
  start_line?: number;
  end_line?: number;
  function_type?: string;
  is_async?: boolean;
  coverage_percent?: number;
  coverage_status?: string;
  executable_lines?: number;
  covered_lines?: number;
}

export interface DetectGapsResponse {
  success: boolean;
  total_functions?: number;
  covered?: number;
  partial?: number;
  uncovered?: number;
  functions?: GapFunctionData[];
  message?: string;
}

export interface GeneratedTestData {
  function_id: string;
  function_name: string;
  test_id: string;
  test_code: string;
  model_used: string;
  status: string;
  test_quality_score?: number;
  coverage_percent?: number;
  risk_score?: number;
  potential_coverage_gain?: number;
}

export interface GenerateTestsResponse {
  success: boolean;
  generated_count?: number;
  tests?: GeneratedTestData[];
  message?: string;
}



export interface RiskSummary {
  high_risk: number;
  medium_risk: number;
  low_risk: number;
}

export interface RiskAnalysisResponse {
  success: boolean;
  project_risk_score?: number;
  summary?: RiskSummary;
  functions?: GapFunctionData[];
  message?: string;
}

export interface DependencySummary {
  critical_dependencies: number;
  high_dependencies: number;
  medium_dependencies: number;
  low_dependencies: number;
}

export interface DependencyAnalysisResponse {
  success: boolean;
  summary?: DependencySummary;
  largest_impact_function?: string;
  largest_impact_radius?: number;
  functions?: any[];
  graph?: Record<string, string[]>;
  message?: string;
}

export interface PredictionAnalysisResponse {
  success: boolean;
  current_coverage?: number;
  potential_coverage?: number;
  improvement_potential?: number;
  highest_gain_function?: string;
  highest_gain?: number;
  recommendations?: any[];
  message?: string;
}

export interface ExecutiveDashboardResponse {
  success: boolean;
  project_health_score?: number;
  status?: string;
  coverage?: any;
  risk?: any;
  dependencies?: any;
  testing?: any;
  recommendations?: string[];
  executive_summary?: string;
  top_priority_function?: string;
  highest_risk_function?: string;
  largest_impact_function?: string;
  message?: string;
}

export interface ReportHistoryItem {
  report_id: string;
  uploaded_at: string;
  coverage_percent?: number;
  files_analyzed: number;
  functions_found: number;
  tests_generated: number;
  latest_status?: string;
}

export interface ReportHistoryResponse {
  success: boolean;
  reports: ReportHistoryItem[];
}

export interface ReportSummaryResponse {
  report_id: string;
  coverage_percent?: number;
  files_analyzed: number;
  functions_found: number;
  covered_functions: number;
  partial_functions: number;
  uncovered_functions: number;
  generated_tests: number;
  health_score: number;
  previous_coverage?: number;
  current_coverage?: number;
  coverage_change?: number;
}

export interface ExplainabilityItem {
  function: string;
  coverage?: number;
  risk: string;
  reason: string[];
  generated_test_id?: string;
}

export interface ExplainabilityResponse {
  success: boolean;
  report_id: string;
  explanations: ExplainabilityItem[];
}

export interface GovernanceOverviewResponse {
  success: boolean;
  reports_analyzed: number;
  functions_scanned: number;
  coverage_gaps_found: number;
  tests_generated: number;
  average_coverage: number;
  average_health_score: number;
}

export const reportClient = {
  // ... previous methods ...
  getLatestReport: async (): Promise<{ success: boolean; report_id?: string; message?: string }> => {
    try {
      const response = await axios.get(`${API_URL}/api/reports/latest`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred getting latest report.',
      };
    }
  },

  uploadReport: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/reports/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as UploadResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during upload.',
      };
    }
  },

  analyzeReport: async (reportId: string): Promise<AnalyzeResponse> => {
    try {
      console.log(`[reportClient] POST /api/reports/${reportId}/analyze payload: {}`);
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/analyze`);
      console.log(`[reportClient] analyzeReport response:`, response.data);
      return response.data;
    } catch (error: any) {
      console.error(`[reportClient] analyzeReport error:`, error);
      if (error.response && error.response.data) {
        return error.response.data as AnalyzeResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during analysis.',
      };
    }
  },

  scanCode: async (reportId: string, directoryPath: string): Promise<ScanResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/scan`, {
        directory_path: directoryPath
      });
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as ScanResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during AST scanning.',
      };
    }
  },

  detectGaps: async (reportId: string): Promise<DetectGapsResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/detect-gaps`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as DetectGapsResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during gap detection.',
      };
    }
  },

  generateTests: async (reportId: string, functionIds?: string[]): Promise<GenerateTestsResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/generate-tests`, {
        function_ids: functionIds
      });
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as GenerateTestsResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during test generation.',
      };
    }
  },

  analyzeRisks: async (reportId: string): Promise<RiskAnalysisResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/risk-analysis`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as RiskAnalysisResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during risk analysis.',
      };
    }
  },

  analyzeDependencies: async (reportId: string): Promise<DependencyAnalysisResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/dependency-analysis`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as DependencyAnalysisResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during dependency analysis.',
      };
    }
  },

  predictCoverage: async (reportId: string): Promise<PredictionAnalysisResponse> => {
    try {
      const response = await axios.post(`${API_URL}/api/reports/${reportId}/coverage-prediction`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as PredictionAnalysisResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred during coverage prediction.',
      };
    }
  },

  getExecutiveDashboard: async (reportId: string): Promise<ExecutiveDashboardResponse> => {
    try {
      const response = await axios.get(`${API_URL}/api/reports/${reportId}/executive-dashboard`);
      return response.data;
    } catch (error: any) {
      if (error.response && error.response.data) {
        return error.response.data as ExecutiveDashboardResponse;
      }
      return {
        success: false,
        message: error.message || 'An unexpected error occurred fetching executive dashboard.',
      };
    }
  },

  getReportHistory: async (): Promise<ReportHistoryResponse> => {
    const response = await axios.get(`${API_URL}/api/reports/history`);
    return response.data;
  },

  getReportSummary: async (reportId: string): Promise<ReportSummaryResponse> => {
    const response = await axios.get(`${API_URL}/api/reports/${reportId}/summary`);
    return response.data;
  },

  getExplainability: async (reportId: string): Promise<ExplainabilityResponse> => {
    const response = await axios.get(`${API_URL}/api/explainability/report/${reportId}`);
    return response.data;
  },

  getGovernanceOverview: async (): Promise<GovernanceOverviewResponse> => {
    const response = await axios.get(`${API_URL}/api/governance/overview`);
    return response.data;
  },
};
