import { Question } from "../../types/data"; 

type ContentProps = {
  question: Question
}

export default function Content({ question } : ContentProps) {
  // TODO: Implement the content component to render out the content and sources
  return (
    <div className="rounded-md border-2 border-white/40 p-4">
      <div className="question-section">
        <h2><b>Question:</b></h2>
        <i>"{question.question}"</i>
      </div>

      <div className="question-section">
        <h2><b>Answer:</b></h2>
        <div dangerouslySetInnerHTML={{__html: question.content}} className="question-answer"></div>
      </div>

      <div className="question-section">
        <h2><b>Sources:</b></h2>
        {question.sources.map((el) => {
          return (
          <div className="source-container">
              {
                //the below length check silencing a warning next gives for an empty source, as in the backend
                //some sources returned Unauthorized when trying to get their icons, so could not be populated
              }
              <img src = {el.icon.length > 0 ? el.icon : undefined} className="source-icon"/>
              <a href={el.source} className="source-link">{el.title}</a>
          </div>
          )})}
        </div>
    </div>
  );
}
