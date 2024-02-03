% muhammet ali topcu
% 2020400147
% compiling: yes
% complete: yes

distance(0, 0, 0).  % a dummy predicate to make the sim work.

% distance(Agent, TargetAgent, Distance).
distance(Agent, TargetAgent, Distance) :- Distance is abs(Agent.y - TargetAgent.y) + abs(Agent.x - TargetAgent.x) .




% multiverse_distance(StateId, AgentId, TargetStateId, TargetAgentId, Distance).
multiverse_distance(StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    state(TargetStateId, TargetAgents, _, _),
    TargetAgent = TargetAgents.get(TargetAgentId),
    (Agent.class = wizard -> TravelCost = 2; TravelCost = 5),
    distance(Agent, TargetAgent, DistanceXY),
    history(StateId, _, Time1, _),
    history(TargetStateId, _, Time2, _),
    history(StateId, UniverseId1, _, _),
    history(TargetStateId, UniverseId2, _, _),
    Distance is DistanceXY + TravelCost * (abs(Time1 - Time2) + abs(UniverseId1 - UniverseId2)).



% nearest_agent(StateId, AgentId, NearestAgentId, Distance).

% If agent is not itself, check if it is nearest
helper_nearest_agent(Agent, Agents, [AgentId | AgentIds], NearestAgentId, Distance) :-
    TargetAgent = Agents.get(AgentId),
    TargetAgent.name \= Agent.name,
    distance(Agent, TargetAgent, DistanceToTargetAgent),
    helper_nearest_agent(Agent, Agents, AgentIds, NearestAgentId1, Distance1),
    (DistanceToTargetAgent =< Distance1 ->
        NearestAgentId = AgentId,
        Distance = DistanceToTargetAgent
    ;
        NearestAgentId = NearestAgentId1,
        Distance = Distance1
    ).

% If TargetAgent.name = Agent.name, skip it.
helper_nearest_agent(Agent, Agents, [_ | AgentIds], NearestAgentId, Distance) :-
    helper_nearest_agent(Agent, Agents, AgentIds, NearestAgentId, Distance).

% Base condition, where distance is max.
helper_nearest_agent(_, _, [], _, Distance):-
     Distance = 2147483647.

nearest_agent(StateId, AgentId, NearestAgentId, Distance) :-
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    dict_keys(Agents, AgentIds),
    helper_nearest_agent(Agent, Agents, AgentIds, NearestAgentId, Distance).




% nearest_agent_in_multiverse(StateId, AgentId, TargetStateId, TargetAgentId, Distance).

nearest_agent_in_multiverse(StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    findall(
        TempStateId,
        history(TempStateId, _, _, _),
        StateIdList
    ),
    helper_nearest_agent_in_multiverse(StateIdList, StateId, AgentId, TempTargetStateId, TempTargetAgentId, TempDistance),
    % If current state has same min dist, return it. So, current state has priority.
    nearest_agent_in_state(StateId, StateId, AgentId, CurrentTargetStateId, CurrentTargetAgentId, CurrentDistance),
    (CurrentDistance =< TempDistance ->
         TargetStateId = CurrentTargetStateId,
         TargetAgentId = CurrentTargetAgentId,
         Distance = CurrentDistance
    ;    TargetStateId = TempTargetStateId,
         TargetAgentId = TempTargetAgentId,
         Distance = TempDistance
    ).

helper_nearest_agent_in_multiverse([TempStateId | StateIdList], StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    % Get the nearest in the TempState.
    nearest_agent_in_state(TempStateId, StateId, AgentId, TargetStateId1, TargetAgentId1, Distance1),
    % Send the rest forward.
    helper_nearest_agent_in_multiverse(StateIdList, StateId, AgentId, TempTargetStateId, TempTargetAgentId, TempDistance),
    % After recursive calls, in each exit, check with the nearest agent in this state and the state just exited.
    (TempDistance =< Distance1 ->
        TargetStateId = TempTargetStateId,
        TargetAgentId = TempTargetAgentId,
        Distance = TempDistance
    ;
        TargetStateId = TargetStateId1,
        TargetAgentId = TargetAgentId1,
        Distance = Distance1
    ).

% Base condition, distance is max.
helper_nearest_agent_in_multiverse([], _, _, _, _, Distance):-
     Distance = 2147483647.

% Finds nearest one in certain state.
nearest_agent_in_state(TriedStateId, StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    state(StateId, _, _, _),
    state(TriedStateId, TargetAgents, _, _),
    dict_keys(TargetAgents, TargetAgentIds),
    helper_nearest_agent_in_state(TargetAgentIds, TriedStateId, StateId, AgentId, TargetStateId, TargetAgentId, Distance).

helper_nearest_agent_in_state([TempAgentId | TargetAgentIds], TriedStateId, StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    state(TriedStateId, TargetAgents, _, _),
    TargetAgent = TargetAgents.get(TempAgentId),
    TargetAgent.name \= Agent.name,
    multiverse_distance(StateId, AgentId, TriedStateId, TempAgentId, DistanceToTargetAgent),
    helper_nearest_agent_in_state(TargetAgentIds, TriedStateId, StateId, AgentId, TempTargetStateId, TempTargetAgentId, TempDistance),
    (DistanceToTargetAgent =< TempDistance ->
        TargetStateId = TriedStateId,
        TargetAgentId = TempAgentId,
        Distance = DistanceToTargetAgent
    ;
        TargetStateId = TempTargetStateId,
        TargetAgentId = TempTargetAgentId,
        Distance = TempDistance
    ).
    
helper_nearest_agent_in_state([], _, _, _, _, _, Distance):-
     Distance = 2147483647.

% If a TempAgentId doesn't meet the conditions, skip it.
helper_nearest_agent_in_state([_ | TargetAgentIds], TriedStateId, StateId, AgentId, TargetStateId, TargetAgentId, Distance) :-
    helper_nearest_agent_in_state(TargetAgentIds, TriedStateId, StateId, AgentId, TargetStateId, TargetAgentId, Distance).


% num_agents_in_state(StateId, Name, NumWarriors, NumWizards, NumRogues).

helper_num_agents_in_state(_, [], _, 0, 0, 0).

helper_num_agents_in_state(Agents, [AgentId | AgentsIdList], Name, NumWarriors, NumWizards, NumRogues) :-
    Agent = Agents.get(AgentId),
    Agent.name \= Name,
    (Agent.class = warrior ->
        helper_num_agents_in_state(Agents, AgentsIdList, Name, TempNumWarriors, NumWizards, NumRogues),
        NumWarriors is TempNumWarriors + 1
    ; Agent.class = wizard ->
        helper_num_agents_in_state(Agents, AgentsIdList, Name, NumWarriors, TempNumWizards, NumRogues),
        NumWizards is TempNumWizards + 1
    ; Agent.class = rogue ->
        helper_num_agents_in_state(Agents, AgentsIdList, Name, NumWarriors, NumWizards, TempNumRogues),
        NumRogues is TempNumRogues + 1
    ).

helper_num_agents_in_state(Agents, [_ | AgentsIdList], Name, NumWarriors, NumWizards, NumRogues) :-
    helper_num_agents_in_state(Agents, AgentsIdList, Name, NumWarriors, NumWizards, NumRogues).

num_agents_in_state(StateId, Name, NumWarriors, NumWizards, NumRogues) :-
    state(StateId, Agents, _, _),
    dict_keys(Agents, AgentsIdList),
    helper_num_agents_in_state(Agents, AgentsIdList, Name, NumWarriors, NumWizards, NumRogues).

% difficulty_of_state(StateId, Name, AgentClass, Difficulty).

difficulty_of_state(StateId, Name, AgentClass, Difficulty) :-
    num_agents_in_state(StateId, Name, NumWarriors, NumWizards, NumRogues),
    (AgentClass = warrior ->
        Difficulty is (5 * NumWarriors + 8 * NumWizards + 2 * NumRogues)
    ; AgentClass = wizard ->
        Difficulty is (2 * NumWarriors + 5 * NumWizards + 8 * NumRogues)
    ; AgentClass = rogue ->
        Difficulty is (8 * NumWarriors + 2 * NumWizards + 5 * NumRogues)
    ).



% easiest_traversable_state(StateId, AgentId, TargetStateId, Difficulty).

check_for_traversal_portal(StateId, AgentId, TargetStateId, Difficulty) :-
    state(StateId, Agents, _, TurnOrder),
    Agent = Agents.get(AgentId),

    % check whether global universe limit has been reached
    global_universe_id(GlobalUniverseId),
    universe_limit(UniverseLimit),
    GlobalUniverseId < UniverseLimit,

    % agent cannot time travel if there is only one agent in the universe
    length(TurnOrder, NumAgents),
    NumAgents > 1,

    history(StateId, UniverseId, Time, _),
    history(TargetStateId, TargetUniverseId, TargetTime, _),
    % check whether target is now or in the past
    current_time(TargetUniverseId, TargetUniCurrentTime, _),
    TargetTime < TargetUniCurrentTime,

    % check whether there is enough mana
    (Agent.class = wizard -> TravelCost = 2; TravelCost = 5),
    Cost is abs(TargetTime - Time)*TravelCost + abs(TargetUniverseId - UniverseId)*TravelCost,
    Agent.mana >= Cost,
    % check whether the target location is occupied
    get_earliest_target_state(TargetUniverseId, TargetTime, TargetStateId),
    state(TargetStateId, TargetAgents, _, TargetTurnOrder),
    TargetState = state(TargetStateId, TargetAgents, _, TargetTurnOrder),
    \+tile_occupied(Agent.x, Agent.y, TargetState),

    %Calc Difficulty
    difficulty_of_state(TargetStateId, Agent.name, Agent.class, Difficulty),
    Difficulty > 0.

check_for_traversal_portal(_, _, _, Difficulty) :-
    % If above is not used, return max value for difficulty
    Difficulty = 2147483647, !.

check_for_traversal_portal_to_now(StateId, AgentId, TargetStateId, Difficulty) :-
    state(StateId, Agents, _, TurnOrder),
    Agent = Agents.get(AgentId),

    % agent cannot time travel if there is only one agent in the universe
    length(TurnOrder, NumAgents),
    NumAgents > 1,

    history(StateId, UniverseId, Time, _),
    history(TargetStateId, TargetUniverseId, TargetTime, _),
    % agent can only travel to now if it's the first turn in the target universe
    current_time(TargetUniverseId, TargetTime, 0),
    % agent cannot travel to current universe's now (would be a no-op)
    \+(TargetUniverseId = UniverseId),

    % check whether there is enough mana
    (Agent.class = wizard -> TravelCost = 2; TravelCost = 5),
    Cost is abs(TargetTime - Time)*TravelCost + abs(TargetUniverseId - UniverseId)*TravelCost,
    Agent.mana >= Cost,
    % check whether the target location is occupied
    get_latest_target_state(TargetUniverseId, TargetTime, TargetStateId),
    state(TargetStateId, TargetAgents, _, TargetTurnOrder),
    TargetState = state(TargetStateId, TargetAgents, _, TargetTurnOrder),
    \+tile_occupied(Agent.x, Agent.y, TargetState),

    %Calc Difficulty
    difficulty_of_state(TargetStateId, Agent.name, Agent.class, Difficulty),
    Difficulty > 0.

check_for_traversal_portal_to_now(_, _, _, Difficulty) :-
    % If above is not used, return max value for difficulty
    Difficulty = 2147483647, !.

check_for_traversal(StateId, AgentId, TargetStateId, Difficulty, Action) :-
    check_for_traversal_portal(StateId, AgentId, TempTargetStateId1, TempDifficulty1),
    check_for_traversal_portal_to_now(StateId, AgentId, TempTargetStateId2, TempDifficulty2),
    (TempDifficulty2 < TempDifficulty1 ->
         TargetStateId = TempTargetStateId2,
         Difficulty = TempDifficulty2,
         Action = portal_to_now
    ;
         TargetStateId = TempTargetStateId1,
         Difficulty = TempDifficulty1,
         Action = portal
    ).


find_easiest_traversable_state([], _, _, -1, 2147483647).

find_easiest_traversable_state([TempStateId | StateIds], StateId, AgentId, TargetStateId, Difficulty) :-
    check_for_traversal(StateId, AgentId, TempStateId, CalculatedDifficulty, _),
    find_easiest_traversable_state(StateIds, StateId, AgentId, TempTargetStateId, TempDifficulty),
    (CalculatedDifficulty =< TempDifficulty ->
         TargetStateId = TempStateId,
         Difficulty = CalculatedDifficulty
    ;
         TargetStateId = TempTargetStateId,
         Difficulty = TempDifficulty
    ).

easiest_traversable_state(StateId, AgentId, TargetStateId) :-
    findall(
        CandidateStateId,
        history(CandidateStateId, _, _, _),
        CandidateStateIds
    ),
    find_easiest_traversable_state(CandidateStateIds, StateId, AgentId, TempTargetStateId, _),
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    difficulty_of_state(TempTargetStateId, Agent.name, Agent.class, TempTargetStateDifficulty),
    difficulty_of_state(StateId, Agent.name, Agent.class, CurrentStateDifficulty),
    (CurrentStateDifficulty =< TempTargetStateDifficulty ->
        TargetStateId = StateId
        ;
        TargetStateId = TempTargetStateId
    ).


% basic_action_policy(StateId, AgentId, Action).

attack_helper(StateId, AgentId, Action) :-
    nearest_agent(StateId, AgentId, NearestAgentId, Distance),
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    (Agent.class = warrior ->
        Distance =< 1,
        Action = [melee_attack, NearestAgentId]
    ; Agent.class = wizard ->
        Distance =< 10,
        Action = [magic_missile, NearestAgentId]
    ; Agent.class = rogue ->
        Distance =< 5,
        Action = [ranged_attack, NearestAgentId]
    ).

%If cannot attack, move
attack_helper(StateId, AgentId, Action) :-
    nearest_agent(StateId, AgentId, NearestAgentId, Distance),
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    TargetAgent = Agents.get(NearestAgentId),
    (
     abs(Agent.y - TargetAgent.y) + abs(Agent.x + 1 - TargetAgent.x) < Distance -> Action = [move_right] ;
     abs(Agent.y + 1 - TargetAgent.y) + abs(Agent.x - TargetAgent.x) < Distance -> Action = [move_up] ;
     abs(Agent.y - TargetAgent.y) + abs(Agent.x - TargetAgent.x - 1) < Distance -> Action = [move_left] ;
     abs(Agent.y - TargetAgent.y - 1) + abs(Agent.x - TargetAgent.x) < Distance -> Action = [move_down]
    ).

%If cannot move, rest
attack_helper(_, _, Action) :-
     Action = [rest].


basic_action_policy(StateId, AgentId, Action) :-
    easiest_traversable_state(StateId, AgentId, TargetStateId),
    check_for_traversal(StateId, AgentId, TargetStateId, Difficulty, TempAction),
    state(StateId, Agents, _, _),
    Agent = Agents.get(AgentId),
    difficulty_of_state(StateId, Agent.name, Agent.class, Difficulty2),
    (TargetStateId = -1 ->
         % Don't portal
         attack_helper(StateId, AgentId, Action)
    ; (Difficulty2 =< Difficulty, Difficulty2 > 0) ->
         % Don't portal
         attack_helper(StateId, AgentId, Action)
    ; Difficulty = 2147483647 ->
         % Don't portal
         attack_helper(StateId, AgentId, Action)
    ;
         % Portal or Portal_to_now
         history(TargetStateId, TargetUniverseId, _, _),
         Action = [TempAction, TargetUniverseId]
    ).

