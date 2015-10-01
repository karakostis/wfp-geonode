update base_resourcebase set owner_id = 2 where owner_id is Null;

delete from layers_layer where resourcebase_ptr_id in (3,4,5,6,7);
