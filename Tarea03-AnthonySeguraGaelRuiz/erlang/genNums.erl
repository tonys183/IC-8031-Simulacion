-module(genNums).
-export([main/0]).

main() ->
    {ok, File} = file:open("erlang.txt", [write, delayed_write]),
    gen(File, 1000000),
    file:close(File).

gen(_File, 0) -> ok;
gen(File, N) -> io:format(File, "~.16f~n", [rand:uniform()]), gen(File, N-1).