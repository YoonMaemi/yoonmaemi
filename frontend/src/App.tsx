// React와 관련된 훅(hook)들을 가져옵니다.
import { FormEvent, useEffect, useMemo, useState } from "react";
// API 통신을 위한 함수들과 메시지 타입을 가져옵니다.
import { fetchHistory, Message, sendMessage } from "./api";
// 애플리케이션의 기본 스타일을 가져옵니다.
import "./App.css";

/**
 * 메시지 역할(role)에 따라 표시할 레이블을 반환하는 함수입니다.
 * @param role 메시지 역할 ("user" 또는 "model")
 * @returns "사용자" 또는 "요약" 문자열
 */
function formatRoleLabel(role: Message["role"]) {
  return role === "user" ? "사용자" : "요약";
}

/**
 * 애플리케이션의 메인 컴포넌트입니다.
 */
function App(): JSX.Element {
  // 상태(State) 변수들을 선언합니다.
  const [history, setHistory] = useState<Message[]>([]); // 대화 기록을 저장하는 상태
  const [input, setInput] = useState(""); // 사용자가 입력한 텍스트를 저장하는 상태
  const [isLoading, setIsLoading] = useState(false); // API 요청이 진행 중인지 여부를 나타내는 상태
  const [error, setError] = useState<string | null>(null); // 오류 메시지를 저장하는 상태

  // 컴포넌트가 처음 렌더링될 때 대화 기록을 가져옵니다.
  useEffect(() => {
    fetchHistory()
      .then(setHistory) // 성공하면 history 상태를 업데이트합니다.
      .catch((err) => setError(err instanceof Error ? err.message : String(err))); // 실패하면 error 상태를 업데이트합니다.
  }, []); // 빈 배열을 전달하여 컴포넌트가 마운트될 때 한 번만 실행되도록 합니다.

  // 제출 버튼 활성화 여부를 결정하는 변수입니다.
  // 입력값이 비어있지 않고, 로딩 중이 아닐 때만 true가 됩니다.
  const canSubmit = useMemo(() => input.trim().length > 0 && !isLoading, [input, isLoading]);

  /**
   * 폼(form) 제출 시 호출되는 이벤트 핸들러입니다.
   * @param event 폼 제출 이벤트 객체
   */
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); // 폼의 기본 제출 동작(페이지 새로고침)을 막습니다.
    if (!canSubmit) {
      return; // 제출할 수 없는 상태이면 함수를 종료합니다.
    }

    setIsLoading(true); // 로딩 상태를 true로 설정합니다.
    setError(null); // 이전 오류 메시지를 초기화합니다.

    try {
      // API를 통해 메시지를 전송하고 결과를 받습니다.
      const result = await sendMessage(input.trim());
      setHistory(result.history); // 반환된 대화 기록으로 상태를 업데이트합니다.
      setInput(""); // 입력창을 비웁니다.
    } catch (err) {
      // 오류 발생 시 error 상태를 업데이트합니다.
      setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      // API 요청이 성공하든 실패하든 로딩 상태를 false로 설정합니다.
      setIsLoading(false);
    }
  }

  // 화면에 렌더링할 JSX를 반환합니다.
  return (
    <div className="page">
      <header>
        <h1>세 줄 요약 데모</h1>
        <p>문장을 입력하면 Gemini가 핵심을 세 줄로 정리합니다.</p>
      </header>

      <main>
        {/* 대화 기록을 표시하는 섹션 */}
        <section className="history">
          {history.length === 0 ? (
            <p className="empty">아직 대화가 없습니다. 첫 요약을 요청해보세요!</p>
          ) : (
            history.map((message, index) => (
              <article key={index} className={`message ${message.role}`}>
                <span className="label">{formatRoleLabel(message.role)}</span>
                <p>{message.content}</p>
              </article>
            ))
          )}
        </section>

        {/* 사용자 입력을 받는 폼 */}
        <form onSubmit={handleSubmit} className="composer">
          <label htmlFor="input">요약할 문장</label>
          <textarea
            id="input"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="요약을 원하는 문장을 입력하세요."
            rows={5}
          />
          <div className="actions">
            <button type="submit" disabled={!canSubmit}>
              {isLoading ? "요약 중..." : "세 줄로 요약하기"}
            </button>
          </div>
        </form>

        {/* 오류 메시지를 표시하는 부분 */}
        {error && <p className="error">⚠️ {error}</p>}
      </main>
    </div>
  );
}

// App 컴포넌트를 다른 파일에서 사용할 수 있도록 내보냅니다.
export default App;