import Image from "next/image";
import { Suspense } from "react";

import Content from "./_components/Content";
import { Question } from "../types/data"; 

import '../styles/main.css';

async function ContentList() {
  // TODO: Fetch the data from the backend (http://localhost:8000/data)
  const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/data`);
  const data: Question[] = await res.json();
  console.log(data)

  // Each piece of content in the list should have its own Content component
  return data.map((el,ind) => {
    //I wish there was a database id I could use here, and I could easily add one, but would need to update all the schemas,
    //and I dont have time for that.
    return <Content key={ind} question={el}/>
  })
}

export default function Home() {
  return (
    <main className="mx-auto flex max-w-3xl flex-col items-center gap-8 p-8">
      <div className="flex flex-col items-center text-center">
        <Image
          src="/logo.png"
          alt="Citizens Advice SORT"
          width={150}
          height={150}
          priority
        />
        <h1 className="mt-4 text-2xl font-bold">Citizens Advice SORT</h1>
        <h2 className="text-lg font-medium">Junior Developer Practical</h2>
      </div>
      {/* Anything that fetches data goes inside Suspense, which shows the fallback until it's ready */}
      <Suspense fallback={<p>Loading...</p>}>
        <ContentList />
      </Suspense>
    </main>
  );
}
