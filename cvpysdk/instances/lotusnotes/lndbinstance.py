# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""File for operating on a Lotus Notes Database Agent Instance.

LNDBInstance is the only class defined in this file.

LNDBInstance:
    restore_in_place()                  --  performs an in place restore of the subclient

    restore_out_of_place()              --  performs an out of place restore of the subclient

    _restore_common_options_json()      --  setter for  the Common options in restore JSON

    _restore_json()                     --  returns the JSON request to pass to the API
    as per the options selected by the user

"""

from __future__ import unicode_literals

from .lninstance import LNInstance
from ...exception import SDKException


class LNDBInstance(LNInstance):
    """Derived class from LNInstance Base class, representing an LNDB instance,
        and to perform operations on that instance."""

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "doNotReplayTransactLogs": value.get('common_options_dict').get(
                'doNotReplayTransactLogs', False
            ),
            "clusterDBBackedup": value.get('common_options_dict').get(
                'clusterDBBackedup', False
            ),
            "recoverWait": value.get('common_options_dict').get(
                'recoverWait', False
            ),
            "restoreToDisk": value.get('common_options_dict').get(
                'restoreToDisk', False
            ),
            "offlineMiningRestore": value.get('common_options_dict').get(
                'offlineMiningRestore', False
            ),
            "restoreToExchange": value.get('common_options_dict').get(
                'restoreToExchange', False
            ),
            "recoverZapIfNecessary": value.get('common_options_dict').get(
                'recoverZapIfNecessary', False
            ),
            "recoverZapReplica": value.get('common_options_dict').get(
                'recoverZapReplica', False
            ),
            "copyToObjectStore": value.get('common_options_dict').get(
                'copyToObjectStore', False
            ),
            "onePassRestore": value.get('common_options_dict').get(
                'onePassRestore', False
            ),
            "recoverZap": value.get('common_options_dict').get(
                'recoverZap', False
            ),
            "recoverRefreshBackup": value.get('common_options_dict').get(
                'recoverRefreshBackup', False
            ),
            "unconditionalOverwrite": value.get('common_options_dict').get(
                'unconditionalOverwrite', False
            ),
            "syncRestore": value.get('common_options_dict').get(
                'syncRestore', False
            ),
            "recoverPointInTime": value.get('common_options_dict').get(
                'recoverPointInTime', False
            )
        }

        if value.get('common_options_dict').get('disasterRecovery'):
            self._commonoption_restore_json.update({
                "restoreDeviceFilesAsRegularFiles": value.get('common_options_dict').get(
                    'restoreDeviceFilesAsRegularFiles', False
                ),
                "isFromBrowseBackup": value.get('common_options_dict').get(
                    'isFromBrowseBackup', False
                ),
                "ignoreNamespaceRequirements": value.get('common_options_dict').get(
                    'ignoreNamespaceRequirements', False
                ),
                "restoreSpaceRestrictions": value.get('common_options_dict').get(
                    'restoreSpaceRestrictions', False
                ),
                "skipErrorsAndContinue": value.get('common_options_dict').get(
                    'skipErrorsAndContinue', False
                ),
                "recoverAllProtectedMails": value.get('common_options_dict').get(
                    'recoverAllProtectedMails', False
                ),
                "validateOnly": value.get('common_options_dict').get(
                    'validateOnly', False
                ),
                "revert": value.get('common_options_dict').get(
                    'revert', False
                ),
                "disasterRecovery": value.get('common_options_dict').get(
                    'disasterRecovery', True
                ),
                "detectRegularExpression": value.get('common_options_dict').get(
                    'detectRegularExpression', True
                ),
            })

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

                   Args:
                       kwargs   (list)  --  list of options need to be set for restore

                   Returns:
                       dict - JSON request to pass to the API
               """
        restore_json = super(LNDBInstance, self)._restore_json(**kwargs)

        restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'lotusNotesDBRestoreOption'] = {
                "disableReplication": kwargs.get('lndb_restore_options').get(
                    'disableReplication', False
                ),
                "disableBackgroundAgents": kwargs.get('lndb_restore_options').get(
                    'disableBackgroundAgents', False
                )
            }

        if kwargs.get('common_options_dict').get('disasterRecovery'):
            restore_json['taskInfo']['subTasks'][0]['options']['commonOpts'] = {
                'jobDescription': '',
                'startUpOpts': {
                    'startInSuspendedState': False,
                    'useDefaultPriority': True,
                    'priority': 166
                }
            }
            restore_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = {
                'backupLevel': 2
            }
            restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'browseOption']['mediaOption']['copyPrecedence'] = {
                    'copyPrecedence': 0,
                    'synchronousCopyPrecedence': 1,
                    'copyPrecedenceApplicable': False
                }
        return restore_json

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            **kwargs):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time               (str)   --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                common_options_dict     (dict)  -- dictionary for all the common options
                    options:
                        unconditionalOverwrite              :   overwrite the files during restore
                        even if they exist

                        recoverWait                         :   Specifies whether this restore
                        operation must wait until resources become available if a database recovery
                        is already taking place

                        recoverZap                          :   Specifies whether the IBM Domino
                        must change the DBIID associated with the restored database

                        recoverZapReplica                   :   Specifies whether the restore
                        operation changes the replica id of the restored database

                        recoverZapIfNecessary               :   Specifies whether the IBM Domino
                        can change the DBIID associated with the restored database if necessary

                        doNotReplayTransactLogs             :   option to skip restoring or
                        replaying logs


                    Disaster Recovery special options:
                        skipErrorsAndContinue               :   enables a data recovery operation
                        to continue despite media errors

                        disasterRecovery                    :   run disaster recovery

                lndb_restore_options    (dict)  -- dictionary for all options specific
                to an lndb restore
                    options:
                        disableReplication      :   disable relpication on database

                        disableBackgroundAgents :   disable background agents

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        return super(LNDBInstance, self).restore_in_place(
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            **kwargs):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore

                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files

                    default: True

                copy_precedence         (int)      --  copy precedence value of storage policy copy

                    default: None

                from_time               (str)       --  time to retore the contents after

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)       --  time to retore the contents before

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                 common_options_dict    (dict)      -- dictionary for all the common options
                    options:
                        unconditionalOverwrite              :   overwrite the files during restore
                        even if they exist

                        recoverWait                         :   Specifies whether this restore
                        operation must wait until resources become available if a database recovery
                        is already taking place

                        recoverZap                          :   Specifies whether the IBM Domino
                        must change the DBIID associated with the restored database

                        recoverZapReplica                   :   Specifies whether the restore
                        operation changes the replica id of the restored database

                        recoverZapIfNecessary               :   Specifies whether the IBM Domino
                        can change the DBIID associated with the restored database if necessary

                        doNotReplayTransactLogs             :   option to skip restoring or
                        replaying logs


                    Disaster Recovery special options:
                        skipErrorsAndContinue               :   enables a data recovery operation
                        to continue despite media errors

                        disasterRecovery                    :   run disaster recovery

                lndb_restore_options    (dict)      -- dictionary for all options specific
                to an lndb restore
                    options:
                        disableReplication      :   disable relpication on database

                        disableBackgroundAgents :   disable background agents

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        return super(LNDBInstance, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)
