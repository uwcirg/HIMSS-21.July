// app theme colors
var appTheme = {
    themes: {
        light: {
            base: "#37353a",
            primary: '#5D6B86',
            secondary: '#718D39',
            accent: '#F8F8F8',
            bgColor: '#37516A'
        }
    }
};
var appData = {
    theme: appTheme
};
var API_BASE_URL = "";
new Vue({
  el: '#app',
  vuetify: new Vuetify(appData),
  data: function() {
    return {
            apiURL: API_BASE_URL + "/Patient",
            //apiURL: "./data/data.json", //for mock data
            initialized: false,
            alert: false,
            dialog: false,
            expanded: [],
            tab: "tab_eicr",
            activeItem: {
                first_name: "",
                last_name: "",
                birthdate: "",
                reason_for_report: "",
                reportable_condition: "",
                EICRLink: "",
                RRLink: ""
            },
            defaultItem: {
                first_name: "",
                last_name: "",
                birthdate: "",
                reason_for_report: "",
                reportable_condition: "",
                EICRLink: "",
                RRLink: ""
            },
            search: '',
            date_of_report: "",
            first_name: "",
            last_name: "",
            gender: "",
            birthdate: "",
            reason_for_report: "",
            reportable_condition: "",
            jurisdiction: "",
            loading: false,
            eicrViewerLoaded: false,
            rrViewerLoaded: false,
            sortBy: 'date_of_report',
            excludeFields: ["address", "city", "doc_id", "ethnicity", "id", "phone", "provider", "race", "state", "zip", "uuid", "EICRLink", "RRLink", "link"],
            demoDataFields: [
                "last_name", "first_name","birthdate", "gender"
            ],
            discreteDataFields: [
                "date_of_report", "reportable_condition", "reason_for_report"
            ],
            headers: [
                {
                    "text": "Date Reported",
                    "value": "date_of_report",
                    filter: value => {
                        if (!this.date_of_report) return true;
                        return String(value).toLowerCase().indexOf(String(this.date_of_report).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "Condition",
                    "value": "reportable_condition",
                    filter: value => {
                        if (!this.reportable_condition) return true;
                        return String(value).toLowerCase().indexOf(String(this.reportable_condition).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "Last Name",
                    "value": "last_name",
                    filter: value => {
                        if (!this.last_name) return true;
                        return String(value).toLowerCase().indexOf(String(this.last_name).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "First Name",
                    "value": "first_name",
                    filter: value => {
                        if (!this.first_name) return true;
                        return String(value).toLowerCase().indexOf(String(this.first_name).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "Birth Date",
                    "value": "birthdate",
                    filter: value => {
                        if (!this.birthdate) return true;
                        return String(value).toLowerCase().indexOf(String(this.birthdate).toLowerCase()) >= 0;
                    },
                    "align": "center"
                },
                {
                    "text": "View Reports",
                    "value": "link",
                    filter: false,
                    "align": "center",
                    "complexType": true
                },
            ],
            results: [],
            errorMessage: ""
        }
    },
    watch: {
        dialog (val) {
          val || this.closeDialog()
        }
    },
    mounted: function() {
        var self = this;
        self.sendRequest(this.apiURL).then(function(response) {
            if (response) {
                var responseObj = JSON.parse(response);
                if (responseObj.patients) {
                    self.results = responseObj.patients;
                    self.results = responseObj.patients.map(function(item) {
                        item["link"] = "";
                        item["EICRLink"] = API_BASE_URL+"/static/"+item.uuid+"_eICR.html";
                        item["RRLink"] = API_BASE_URL+"/static/"+item.uuid+"_RR.html";
                        //mock data testing
                        //item["EICRLink"] = "./data/eICR.html";
                        //item["RRLink"] = "./data/RR.html";
                        item["birthdate"] = self.formatDate(item["birthdate"]);
                        item["date_of_report"] = self.formatDate(item["date_of_report"], true);
                        return item;
                    });
                    self.expanded = responseObj.patients.map(function(item, index) {
                        return item;
                    })
                }
                //console.log("self.results ", self.results)
            }
            if (!self.results || !self.results.length) {
                self.setError("No data returned from the server.");
                self.initialized = true;
            }
            setTimeout(function(){
                self.initialized = true;
            }.bind(self), 150);
        }).catch(function(e) {
            self.initialized = true;
            self.setError("Unable to display data. see console for detail. " + (e.status && e.statusText ? (e.status + " " + e.statusText): e));
            console.log("api error ", e)
        });
    },
    methods: {
        setError: function(message) {
            if (message) {
                this.errorMessage = message;
                this.alert = true;
                return;
            }
            this.alert = false;
        },
        formatDate: function(string, includeTime) {
            if (!string) return "";
            var year = string.substr(0, 4);
            var month = string.substr(4, 2);
            var day = string.substr(6, 2);
            var dateString = year+"-"+month+"-"+day;
            if (includeTime) dateString += " "+string.substr(8, 2)+":"+string.substr(10, 2);
            return dateString;
        },
        viewActiveItem: function(item) {
            var self = this;
            this.$nextTick(function() {
                self.activeItem = Object.assign({}, item);
            });
            this.dialog = true;
        },
        closeDialog: function() {
            this.tab = "tab_eicr";
            this.dialog = false;
            var self = this;
            this.$nextTick(function() {
                self.activeItem = Object.assign({}, this.defaultItem);
            })
        },
        inExclusionFields: function(key) {
            return key !== "View Reports" && this.excludeFields.indexOf(key) !== -1;
        },
        inHeaderList: function(key) {
            return this.headers.filter(function(item) {
                return !item.complexType && String(item.value) === String(key);
            }).length > 0;
        },
        getDisplayText: function(key) {
            var matchedField = this.headers.filter(function(item) {
                return String(item.value) === String(key);
            });
            if (!matchedField.length) {
                if (key === "date_of_report") return "Date Reported";
                if (key === "reason_for_report") return "Condition (Full Description)";
                if (key === "reportable_condition") return "Condition";
                return String(key).replace(/_/g, " ");
            }
            return matchedField[0].text;
        },
        sendRequest: function(url, params) {
            params = params || {};
            // Return a new promise.
            return new Promise(function(resolve, reject) {
              // Do the usual XHR stuff
              var req = new XMLHttpRequest();
              req.open('GET', url);
              req.onload = function() {
                // This is called even on 404 etc
                // so check the status
                if (req.status == 200) {
                  // Resolve the promise with the response text
                  resolve(req.response);
                }
                else {
                  // Otherwise reject with the status text
                  // reject with error, which will hopefully be a meaningful message
                  reject(req);
                }
              };

              // Handle network errors
              req.onerror = function() {
                reject(Error("Network Error"));
              };

              // Make the request
              req.send();
            });
        }
    }
});
