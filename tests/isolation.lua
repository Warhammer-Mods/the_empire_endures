-- Run under Lua 5.1 from the repository root.
local listeners, save_keys, first_ticks = {}, {}, {}
core = {add_listener=function(_, name,event,condition,callback,persistent)
 listeners[#listeners+1]={name=name,event=event,condition=condition,callback=callback}
end}
cm = {add_saving_game_callback=function(_, fn) end,
 add_loading_game_callback=function(_, fn) end,
 add_first_tick_callback=function(_,fn) first_ticks[#first_ticks+1]=fn end,
 mission_is_active_for_faction=function() return false end,
 get_faction=function(_,key) return {name=function() return key end} end}
dofile('src/script/campaign/wh3_dlc25_gunnery_school.lua')
local original = gunnery_school
dofile('src/script/campaign/mod/ss_franz_gunnery_school.lua')
assert(gunnery_school == original)
assert(gunnery_school.faction_key == 'wh_main_emp_wissenland')
assert(ss_franz_gunnery_school.faction_key == 'wh_main_emp_empire')
assert(gunnery_school.progression_unlocks ~= ss_franz_gunnery_school.progression_unlocks)
gunnery_school:unlock_panel_progression()
ss_franz_gunnery_school:unlock_panel_progression()
assert(#listeners == 2)
assert(listeners[1].name ~= listeners[2].name)
local function context(key)
 return {faction=function() return {name=function() return key end} end,
 mission=function() return {mission_record_key=function() return 'wh3_dlc25_gunnery_school_tier_1_1' end} end}
end
assert(listeners[1].condition(context('wh_main_emp_empire')) == false)
assert(listeners[2].condition(context('wh_main_emp_wissenland')) == false)
assert(listeners[1].condition(context('wh_main_emp_wissenland')) == true)
assert(listeners[2].condition(context('wh_main_emp_empire')) == true)
ss_franz_gunnery_school.current_stage = 4
assert(gunnery_school.current_stage == 1)
print('PASS: controller, mutable state, listeners and mission ownership isolation')
