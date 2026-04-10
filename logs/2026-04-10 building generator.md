got prompt
!!! Exception during processing !!! Cl_orso_character_sheet_generator_comfyui_bindings.generate() missing 3 required positional arguments: 'i_ls_layout_file_path', 'i_ls_mask_front_path', and 'i_ls_mask_back_path'
Traceback (most recent call last):
  File "D:\ComfyUI\execution.py", line 534, in execute
    output_data, output_ui, has_subgraph, has_pending_tasks = await get_output_data(prompt_id, unique_id, obj, input_data_all, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ComfyUI\execution.py", line 334, in get_output_data
    return_values = await _async_map_node_over_list(prompt_id, unique_id, obj, input_data_all, obj.FUNCTION, allow_interrupt=True, execution_block_cb=execution_block_cb, pre_execute_cb=pre_execute_cb, v3_data=v3_data)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\ComfyUI\execution.py", line 308, in _async_map_node_over_list
    await process_inputs(input_dict, i)
  File "D:\ComfyUI\execution.py", line 296, in process_inputs
    result = f(**inputs)
TypeError: Cl_orso_character_sheet_generator_comfyui_bindings.generate() missing 3 required positional arguments: 'i_ls_layout_file_path', 'i_ls_mask_front_path', and 'i_ls_mask_back_path'