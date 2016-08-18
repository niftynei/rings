-module(ring).
-compile(export_all).

start() ->
  RootPid = spawn(fun() -> head_loop(self()) end),
  _ChildPid = spawn_next(RootPid, RootPid),
  _ChildPid ! {hello},
  RootPid ! {child, _ChildPid},
  RootPid.

spawn_next(RootPid, ParentPid) ->
  spawn(fun() -> loop({RootPid, ParentPid}) end).

head_loop(Pid) ->
  receive
    {child, _Pid} ->
      io:format("Child Pid is ~p~n", [_Pid]),
      head_loop(_Pid); 
    {start, N} ->
      statistics(runtime),
      statistics(wall_clock),
      Pid ! {ring, N},
      head_loop(Pid);
    {send, M} ->
      Pid ! {message, M},
      head_loop(Pid); 
    {message, 0} ->
      % print out how long it took
      {_, Time1} = statistics(runtime),
      {_, Time2} = statistics(wall_clock),
      U1 = Time1 / 1000,
      U2 = Time2 / 1000,
      io:format("finished looping in ~ps (~ps)~n",[U1, U2]),
      head_loop(Pid);
    {message, M} ->
      Pid ! {message, M - 1},
      head_loop(Pid); 
    {done, _Pid} ->
      io:format("Ran out of Ns at ~p~n", [_Pid]),
      head_loop(_Pid);
    Any ->
      io:format("~p Received:~p~n", [self(), Any]),
      head_loop(Pid)
   end.

loop({RootPid, Pid}) ->
  receive
    {ring, 0} ->
      RootPid ! {done, self()},
      loop({RootPid, Pid});
    {ring, N} ->
      _Pid = spawn_next(RootPid, self()),
      io:format("~p started new process ~p~n", [self(), _Pid]),
      _Pid ! {ring, N-1},
      loop({RootPid, Pid});
    {message, M} ->
      Pid ! {message, M},
      loop({RootPid, Pid});      
    Any ->
      io:format("~p Received:~p~n", [self(), Any]),
      RootPid ! {ok},
      loop({RootPid, Pid})
  end.
