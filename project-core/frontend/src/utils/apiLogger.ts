/**
 * Frontend API Call Logger
 * 
 * This utility logs all API calls from the frontend to the backend
 * for debugging and monitoring purposes.
 */

interface APICallLog {
  timestamp: string;
  endpoint: string;
  method: string;
  requestData: any;
  responseData: any;
  statusCode: number;
  responseTime: number;
  error?: string;
}

class APILogger {
  private logs: APICallLog[] = [];
  private maxLogs = 1000; // Keep last 1000 logs in memory

  logAPICall(
    endpoint: string,
    method: string,
    requestData: any,
    responseData: any,
    statusCode: number,
    responseTime: number,
    error?: string
  ) {
    const logEntry: APICallLog = {
      timestamp: new Date().toISOString(),
      endpoint,
      method,
      requestData,
      responseData,
      statusCode,
      responseTime,
      error
    };

    this.logs.push(logEntry);

    // Keep only the last maxLogs entries
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs);
    }

    // Log to console for debugging
    console.log('🔍 API_CALL_LOG:', logEntry);

    // Store in localStorage for persistence
    this.saveLogs();
  }

  private saveLogs() {
    try {
      localStorage.setItem('api_call_logs', JSON.stringify(this.logs));
    } catch (error) {
      console.warn('Failed to save API logs to localStorage:', error);
    }
  }

  loadLogs() {
    try {
      const savedLogs = localStorage.getItem('api_call_logs');
      if (savedLogs) {
        this.logs = JSON.parse(savedLogs);
      }
    } catch (error) {
      console.warn('Failed to load API logs from localStorage:', error);
    }
  }

  getLogs(): APICallLog[] {
    return [...this.logs];
  }

  clearLogs() {
    this.logs = [];
    localStorage.removeItem('api_call_logs');
  }

  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

// Create singleton instance
export const apiLogger = new APILogger();

// Load existing logs on import
apiLogger.loadLogs();

export default apiLogger; 