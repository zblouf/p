
#from z.utils.spiff import db

def import_entities(_db):
	pass

def import_entity_structure(_db, entity_id, customer):
	unit_index = {}
	activity_index = {}
	entity = _db.query_dict("SELECT * FROM MAIN__Company WHERE company_id="+str(entity_id))
	if str(entity['ref_id']).isdigit():
		entity['ref_id'] = int(entity['ref_id'])
	e = Entity( name = entity['name'])
	e.customer = customer
#	if str(entity['ref_active'])!="0":
	e.save()
	id = IdTag(content_object=e, value=entity['company_id'])
	id.save()
	unit_list = _db.query_dict("SELECT * FROM MAIN__Unit WHERE company_id="+str(entity['company_id']))
	for unit in unit_list:
		_ref_valid = False
		if str(unit['ref_id']).isdigit():
			unit['ref_id'] = int(unit['ref_id'])
			

def garbage():
                    if str(entity['ref_active'])!="0":
                        _key_exists = False
                        _key_value = 0
                        if entity_index.has_key(entity['ref_id']):
                                _key_exists = True
                                _key_value = entity_index[entity['ref_id']]
                        print '      Entity "%s" has ref #%s activated (%s, %s)' %(entity['name'], repr(entity['ref_id']), repr(_key_exists), repr(_key_value))
                    if str(entity['ref_active'])!="0" and entity_index.has_key(entity['ref_id']):
                        
                        eref = Entity.objects.get(id=entity_index[entity['ref_id']])
                        print '    Ref active for entity "%s", refering to #%d (%s)' %(entity['name'], entity['ref_id'], e.name)
                        e.ref = eref
                        e.ref_active = True

                    # POSITIONS
                    for position_group in self.db2.query_dict('SELECT * FROM MAIN__PositionRegroupment WHERE company_id=%d' %(entity['company_id'])):
                        pass
                    for position in self.db2.query_dict('SELECT * FROM MAIN__Position WHERE company_id=%d' %(entity['company_id'])):
                        while position['name'] in position_names:
                            position['name'] += '_'
                        position_names.append(position['name'])
                        pos = Position(name=position['name'])
                        pos.entity = e
                        if str(position['employees']).isdigit():
                            pos.people_count = position['employees']
                        pos.save()
                        position_index[position['position_id']] = pos.id
                        i = IdTag(content_object=pos, value=position['position_id'])
                        i.save()

                    # UNITS
                    unit_list = self.db2.query_dict('SELECT * FROM MAIN__Unit WHERE company_id='+str(entity['company_id']))
                    for unit in unit_list:
                        _ref_valid = False
                        if str(unit['ref_id']).isdigit():
                            unit['ref_id'] = int(unit['ref_id'])
                            if unit_index.has_key(unit['ref_id']):
                                _ref_valid = True
                        u = Unit(name = unit['name'])
                        u.entity = e
                        if _ref_valid and Unit.objects.filter(id=unit_index[unit['ref_id']]).count()>0:
                            uref = Unit.objects.get(id=unit_index[unit['ref_id']])
                            u.ref = uref
                        u.save()
                        unit_index[unit['unit_id']] = u.id
                        i = IdTag(content_object=u, value=unit['unit_id'])
                        i.save()
                        activity_list = self.db2.query_dict('SELECT * FROM MAIN__Activity WHERE unit_id='+str(unit['unit_id']))
                        #ACTIVITES
                        for activity in activity_list:
                            _ref_valid = False
                            if str(activity['ref_id']).isdigit():
                                activity['ref_id'] = int(activity['ref_id'])
                                if activity_index.has_key(activity['ref_id']):
                                    _ref_valid = True
                            else:
                                activity['ref_id'] = 0
                            print '      - Activity "%s" refering #%d (%s)' %(activity['name'], activity['ref_id'], repr(_ref_valid))
                            a = Activity(name = activity['name'])
                            a.entity = e
                            a.unit = u
                            if _ref_valid and Activity.objects.filter(id=activity_index[activity['ref_id']]).count()>0:
                                aref = Activity.objects.get(id=activity_index[activity['ref_id']])
                                a.ref = aref
                            a.save()
                            activity_index[activity['activity_id']] = a.id
                            i = IdTag(  content_object=a,
                                        value=activity['activity_id'])
                            i.save()
                            # ACTIVITY EXTENSION (PROFESSIONNAL RISKS)
                            ae = PrevActivityExt(activity=a)
                            if activity['profile_id'] is not None \
                                    and str(activity['profile_id']).isdigit():
                                profile = Profile.objects.get(id=profile_index[int(activity['profile_id'])])
                                ae.profile = profile
                            ae.post_type = activity['post_type']
                            ae.schedule_type = activity['schedule_type']
                            ae.employment_type = activity['employment_type']
                            ae.displays = activity['displays']
                            ae.save()
                            equipment_list = self.db2.query_dict('SELECT * FROM PROF__EquipmentActivity WHERE activity_id='+str(activity['activity_id']))
                            for equipment in equipment_list:
                                eq = Equipment.objects.get(id=equipment_index[equipment['equipment_id']])
                                ae.equipments.add(eq)
                            
#                            ae.save()
