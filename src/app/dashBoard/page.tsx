import Image from "next/image";
import SearchBar from "@/components/dashBoardComponents/searchBar";

export default function dashBoard() {

  return (
    <div>
      <div className=" w-[100vw] h-[100vh] overflow-hidden">
        <div className="flex justify-center w-[100vw]">
          <div>
            <p className="my-[10vh] font-light italic font-inter text-[100px] w-fit [text-shadow:_-2px_2px_8px_rgba(255,255,255,0.4)]">
              SACY TECH.
            </p>
          </div>
        </div>
        <div>
          <SearchBar onSearch={(query: string) => {
            // handle search (e.g., update state or call an API)
            console.log("Search:", query);
          }} />
        </div>
        <div className="ml-[1vw] flex h-[40vh] overflow-hidden">
          <div className="flex text-end items-end">
            <p className="opacity-25">© 2025 Tecnologias SACY — Todos os direitos reservados.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
